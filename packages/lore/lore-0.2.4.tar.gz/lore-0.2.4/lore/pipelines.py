from abc import ABCMeta, abstractmethod
from collections import namedtuple
import os
from os.path import join, exists
import logging

import pickle

from numpy import in1d
from lore import env
from lore.util import timer, timed
from sklearn.model_selection import train_test_split


logger = logging.getLogger(__name__)


Observations = namedtuple('Observations', 'x y')


class CrossValidation(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.name = self.__module__ + '.' + self.__class__.__name__
        self.stratify = None
        self.subsample = None
        self._data_dir = join(env.data_dir, self.name)
        self._data = None
        self._encoders = None
        self._training_data = None
        self._test_data = None
        self._validation_data = None
        self._output_encoder = None
        self._encoded_training_data = None
        self._encoded_validation_data = None
        self._encoded_test_data = None

    def __getstate__(self):
        state = dict(self.__dict__)
        # bloat can be restored via self.__init__() + self.build()
        for bloat in [
            '_data',
            '_training_data',
            '_test_data',
            '_validation_data',
            '_encoded_training_data',
            '_encoded_validation_data'
            '_encoded_test_data',
        ]:
            state[bloat] = None
        return state

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_encoders(self):
        pass

    @abstractmethod
    def get_output_encoder(self):
        pass

    @property
    def encoders(self):
        if self._encoders is None:
            with timer('fit encoders:'):
                self._encoders = self.get_encoders()
                for encoder in self._encoders:
                    encoder.fit(self.training_data)
            
        return self._encoders
    
    @property
    def output_encoder(self):
        if self._output_encoder is None:
            with timer('fit output encoder:'):
                self._output_encoder = self.get_output_encoder()
                self._output_encoder.fit(self.training_data)
            
        return self._output_encoder
    
    @property
    def training_data(self):
        if self._training_data is None:
            self._split_data()
    
        return self._training_data

    @property
    def validation_data(self):
        if self._validation_data is None:
            self._split_data()
    
        return self._validation_data

    @property
    def test_data(self):
        if self._test_data is None:
            self._split_data()
    
        return self._test_data

    @property
    def encoded_training_data(self):
        if not self._encoded_training_data:
            with timer('encode training data:'):
                self._encoded_training_data = self.observations(self.training_data)
    
        return self._encoded_training_data

    @property
    def encoded_validation_data(self):
        if not self._encoded_validation_data:
            with timer('encode validation data:'):
                self._encoded_validation_data = self.observations(self.validation_data)
    
        return self._encoded_validation_data

    @property
    def encoded_test_data(self):
        if not self._encoded_test_data:
            with timer('encode test data:'):
                self._encoded_test_data = self.observations(self.test_data)
    
        return self._encoded_test_data

    def observations(self, data):
        return Observations(x=self.encode_x(data), y=self.encode_y(data))

    @timed(logging.INFO)
    def encode_x(self, data):
        result = {}
        for encoder in self.encoders:
            encoded = encoder.transform(data)
            if hasattr(encoder, 'sequence_length'):
                for i in range(encoder.sequence_length):
                    name = encoder.name + '_' + str(i)
                    result[name] = encoded.apply(encoder.get_token, i=i)
            else:
                result[encoder.name] = encoded
        return result
    
    @timed(logging.INFO)
    def encode_y(self, data):
        return self.output_encoder.transform(data)

    @timed(logging.INFO)
    def decode(self, predictions):
        results = {}
        for encoder in self._output_encoder:
            results[encoder.name] = encoder.reverse_transform(predictions)
        return results

    @timed(logging.INFO)
    def _split_data(self):
        if self._data:
            return
    
        self._data = self.get_data()
        logger.debug('data length: %i' % len(self._data))
    
        if self.subsample:
            logger.debug('subsampling: %s' % self.subsample)
            self._data = self._data.sample(self.subsample)
    
        if self.stratify:
            train_path = join(self._data_dir, 'train_ids.pickle')
            validate_path = join(self._data_dir, 'validate_ids.pickle')
            test_path = join(self._data_dir, 'test_ids.pickle')
            if exists(train_path) and exists(validate_path) and exists(test_path):
                train_ids = pickle.load(open(train_path, "rb"))
                validate_ids = pickle.load(open(validate_path, "rb"))
                test_ids = pickle.load(open(test_path, "rb"))
            else:
                ids = self._data[self.stratify].drop_duplicates()
                test_size = len(ids) // 10
            
                train_ids, validate_ids = train_test_split(
                    ids,
                    test_size=test_size,
                    random_state=1
                )
                train_ids, test_ids = train_test_split(
                    train_ids,
                    test_size=test_size,
                    random_state=1
                )
                if not exists(self._data_dir):
                    os.makedirs(self._data_dir)
                pickle.dump(train_ids, open(train_path, 'wb'))
                pickle.dump(validate_ids, open(validate_path, 'wb'))
                pickle.dump(test_ids, open(test_path, 'wb'))
        
            rows = self._data[self.stratify].values
            self._training_data = self._data.iloc[in1d(rows, train_ids.values)]
            self._validation_data = self._data.iloc[in1d(rows, validate_ids.values)]
            self._test_data = self._data.iloc[in1d(rows, test_ids.values)]
        else:
            test_size = len(self._data) // 10
            self._training_data, self._validation_data = train_test_split(
                self._data,
                test_size=test_size,
                random_state=1
            )
            self._training_data, self._test_data = train_test_split(
                self._training_data,
                test_size=test_size,
                random_state=1
            )
