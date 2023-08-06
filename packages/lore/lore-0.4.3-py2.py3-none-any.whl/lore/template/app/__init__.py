import lore
import lore.caches
import os

lore.env.project = __name__
lore.caches.query_cache.limit = os.environ.get('LORE_QUERY_CACHE_LIMIT', 10000000000)
