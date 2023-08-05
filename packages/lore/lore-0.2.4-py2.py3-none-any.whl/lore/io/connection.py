import hashlib
import inspect
import logging
import os
import re
import sys
import tempfile

from psycopg2 import OperationalError

if sys.version_info.major < 3:
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    ModuleNotFoundError = ImportError

import pandas.io.sql
try:
    import psycopg2
    import psycopg2.extras
except ModuleNotFoundError as e:
    psycopg2 = False

import lore
from lore.util import timer
from lore.caches import query_cached


logger = logging.getLogger(__name__)


class Connection(object):
    UNLOAD_PREFIX = os.path.join(lore.env.name, 'unloads')
    IAM_ROLE = os.environ.get('IAM_ROLE')
    
    def __init__(self, url, connect=True):
        self.__url = url
        self._adapter = None
        self._cursor = None
        if connect:
            self.connect()

    def __enter__(self):
        self._adapter.autocommit = False
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self._adapter.commit()
        else:
            self._adapter.rollback()
        self._adapter.autocommit = True

    def connect(self):
        if self._adapter:
            return
        
        if not psycopg2:
            logger.error('psycopg2 is not installed')
            return

        logger.info(self.__url)

        parsed = urlparse(self.__url)
        self._adapter = psycopg2.connect(
            database=parsed.path[1:],
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
            connect_timeout=1
        )
        self._adapter.autocommit = True
        self._cursor = self._adapter.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
    def close(self):
        if not self._adapter:
            return

        self._adapter.close()
        self._adapter = None
        self._cursor = None

    def execute(self, sql=None, filename=None, **kwargs):
        self.connect()
        self.__execute(self.__prepare(sql, filename, kwargs))

    def select(self, sql=None, filename=None, **kwargs):
        cache = kwargs.pop('cache', False)
        sql = self.__prepare(sql, filename, kwargs)
        return self._select(sql, cache=cache)
        
    @query_cached
    def _select(self, sql):
        self.connect()
        self.__execute(sql)
        return self._cursor.fetchall()

    def unload(self, table, sql=None, filename=None, **kwargs):
        self.connect()

        if sql is None and filename is None:
            filename = os.path.join(
                lore.env.root(), lore.env.project, 'extracts', table + ".sql")
            if not os.path.isfile(filename):
                sql = "SELECT * FROM " + table
            else:
                filename = table
        sql = self.__prepare(sql, filename, kwargs)
        sql = "UNLOAD ('" + sql.replace("'", "\\'") + "') "
        sql += "TO 's3://" + os.path.join(
                lore.io.bucket.name,
                self.UNLOAD_PREFIX,
                table,
                table
                ) + "' "
        
        if Connection.IAM_ROLE:
            sql += "IAM_ROLE '" + Connection.IAM_ROLE + "' "
        sql += "DELIMITER ',' ALLOWOVERWRITE ESCAPE"
        self.__execute(sql)

    def load(self, path, table=None, columns=None):
        self.connect()

        if table is None:
            table = path

        for entry in lore.io.bucket.objects.filter(
            Prefix=os.path.join(self.UNLOAD_PREFIX, path)
        ):
            temp = tempfile.NamedTemporaryFile()
            with timer("SQL COPY: %s -> %s" % (entry.key, table)):
                lore.io.bucket.download_file(entry.key, temp.name)
            temp.seek(0)
            self._cursor.copy_from(temp, table, sep=',', columns=columns)

    def insert(self, sql, tuples):
        self.connect()

        records_list_template = ','.join(['%s'] * len(tuples))
        sql = sql.format(records_list_template)
        sql = self._cursor.mogrify(sql, tuples).decode('utf-8')
        self.__execute(sql)

    def dataframe(self, sql=None, filename=None, **kwargs):
        cache = kwargs.pop('cache', False)
        sql = self.__prepare(sql, filename, kwargs)
        sql = self.__caller_annotation(stack_depth=2) + sql
        return self._dataframe(sql=sql, cache=cache)
        
    @query_cached
    def _dataframe(self, sql):
        self.connect()
        logger.debug(sql)
        with timer("dataframe:"):
            return pandas.io.sql.read_sql(sql=sql, con=self._adapter)

    def etl(self, table, to, **kwargs):
        self.connect()

        self.unload(table, **kwargs)
        with to as transaction:
            transaction.execute("DELETE FROM " + table)
            transaction.load(table)
            transaction.execute("ANALYZE " + table)
        to.execute("ANALYZE " + table)

    def __prepare(self, sql, filename, bindings):
        if sql is None and filename is not None:
            filename = os.path.join(
                lore.env.root, lore.env.project, 'extracts', filename + ".sql")
            logger.debug("READ SQL FILE: " + filename)
            with open(filename) as file:
                sql = file.read()
        # support mustache style bindings
        sql = re.sub(r'\{(\w+?)\}', r'%(\1)s', sql)
        if self._cursor:
            cursor = self._cursor
        else:
            try:
                cursor = psycopg2.extras.DictCursor(conn=psycopg2.extensions.connection(dsn=''))
            except OperationalError:
                self.connect()
                cursor = self._cursor

        return cursor.mogrify(sql, bindings).decode('utf-8')

    def __execute(self, sql):
        sql = self.__caller_annotation() + sql
        logger.debug(sql)
        with timer("sql:"):
            self._cursor.execute(sql)

    def __caller_annotation(self, stack_depth=3):
        caller = inspect.stack()[stack_depth]
        if sys.version_info.major == 3:
            caller = (caller.function, caller.filename, caller.lineno)
        return "/* %s | %s:%d in %s */\n" % (lore.env.project, caller[1], caller[2], caller[0])
