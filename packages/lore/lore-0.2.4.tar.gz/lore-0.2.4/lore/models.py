from abc import ABCMeta, abstractmethod
import logging
import threading

import pandas
import keras
from keras.callbacks import EarlyStopping, TensorBoard, TerminateOnNaN
from keras.layers import Input, Embedding, Dense, Reshape, Concatenate, Dropout
from keras.optimizers import Adam
from sklearn.metrics import mean_absolute_error
import tensorflow
import xgboost
import lore.io
from lore.encoders import Continuous
import lore.serializers
from lore.callbacks import ReloadBest
from lore.util import timer, timed

logger = logging.getLogger(__name__)


class Base(object):
    __metaclass__ = ABCMeta
    
    def __init__(self):
        self.name = self.__module__ + '.' + self.__class__.__name__
        self.pipeline = None

    def __getstate__(self):
        return dict(self.__dict__)

    @abstractmethod
    def fit(self):
        pass
        
    @abstractmethod
    def predict(self, dataframe):
        pass

    @abstractmethod
    def benchmark(self):
        pass

    
class Keras(Base):
    def __init__(self):
        super(Keras, self).__init__()
        
        self.embed_size = 10
        self.width = 1024
        self.hidden_layers = 4
        self.layer_shrink = 0.5
        self.dropout = 0
        self.batch_size = 32
        self.learning_rate = 0.001
        self.decay = 0.
        self.optimizer = None
        self.hidden_activation = 'relu'
        self.hidden_activity_regularizer = None
        self.hidden_bias_regularizer = None
        self.hidden_kernel_regularizer = None
        self.keras = None
        self.gain = None
        self.history = None
        self.monitor = 'val_acc'
        self.loss = 'categorical_crossentropy'
        
    def __getstate__(self):
        state = super(Keras, self).__getstate__()
        # bloat can be restored via self.__init__() + self.build()
        for bloat in [
            'keras',
            'optimizer',
            'history',
            '_tf_graph',
            '_tf_graph_lock',
        ]:
            state[bloat] = None
        return state

    @property
    def description(self):
        return '\n'.join([
            '\n  %s' % self.name,
            '==========================================================',
            '| embed | hidden | layer | layer  |         | model      |',
            '| size  | layers | width | shrink | dropout | parameters |',
            '----------------------------------------------------------',
            '| %5i | %6i | %5i | %6.4f | %7.5f | %10i |' % (
                self.embed_size,
                self.hidden_layers,
                self.width,
                self.layer_shrink,
                self.dropout,
                self.keras.count_params()
            ),
            '=========================================================='
        ])
    
    def callbacks(self):
        return []
    
    @timed(logging.INFO)
    def build(self):
        inputs = self.build_inputs()
        embedding_layer = self.build_embedding_layer(inputs)
        hidden_layers = self.build_hidden_layers(embedding_layer)
        output = self.build_output_layer(hidden_layers)
        
        self.keras = keras.models.Model(inputs=list(inputs.values()), outputs=output)
        self.optimizer = Adam(lr=self.learning_rate, decay=self.decay)
        
        self._tf_graph = tensorflow.get_default_graph()
        self._tf_graph_lock = threading.Lock()

        logger.info('\n\n' + self.description + '\n\n')
    
    @timed(logging.INFO)
    def build_inputs(self):
        inputs = {}
        for encoder in self.pipeline.encoders:
            if hasattr(encoder, 'sequence_length'):
                for i in range(encoder.sequence_length):
                    name = encoder.name + '_' + str(i)
                    inputs[name] = Input(shape=(1,), name=name)
            else:
                inputs[encoder.name] = Input(shape=(1,), name=encoder.name)
        return inputs
    
    @timed(logging.INFO)
    def build_embedding_layer(self, inputs):
        embeddings = {}
        reshape = Reshape(target_shape=(self.embed_size,))
        for encoder in self.pipeline.encoders:
            if isinstance(encoder, Continuous):
                embedding = Dense(self.embed_size, activation='relu')
                embeddings[encoder.name] = embedding(inputs[encoder.name], name='embed_' + encoder.name)
            elif hasattr(encoder, 'sequence_length'):
                for i in range(encoder.sequence_length):
                    name = encoder.name + '_' + str(i)
                    embedding = Embedding(encoder.cardinality(), self.embed_size, name='embed_' + name)
                    embeddings[name] = reshape(embedding(inputs[name]))
            else:
                embedding = Embedding(encoder.cardinality(), self.embed_size, name='embed_' + encoder.name)
                embeddings[encoder.name] = reshape(embedding(inputs[encoder.name]))
        
        return Concatenate()(list(embeddings.values()))
    
    @timed(logging.INFO)
    def build_hidden_layers(self, input_layer):
        hidden_layers = input_layer
        
        width = self.width
        for i in range(self.hidden_layers):
            hidden_layers = Dense(int(width),
                                  activation=self.hidden_activation,
                                  activity_regularizer=self.hidden_activity_regularizer,
                                  kernel_regularizer=self.hidden_kernel_regularizer,
                                  bias_regularizer=self.hidden_bias_regularizer,
                                  name='hidden_%i' % i)(hidden_layers)
            if self.dropout > 0:
                hidden_layers = Dropout(self.dropout)(hidden_layers)
            if self.layer_shrink < 1:
                width *= self.layer_shrink
            else:
                width -= self.layer_shrink
        
        return hidden_layers
    
    @timed(logging.INFO)
    def build_output_layer(self, hidden_layers):
        return Dense(1, activation='sigmoid')(hidden_layers)
    
    @timed(logging.INFO)
    def fit(self, epochs=100, patience=0, verbose=None, min_delta=0, tensorboard=False):
        if not self.keras or not self.optimizer:
            self.build()
            
        self.keras.compile(loss=self.loss, optimizer=self.optimizer)
        if verbose is None:
            verbose = 1 if lore.env.name == lore.env.DEVELOPMENT else 0
        
        logger.info(
            '\n'.join([
                '\n\n\n  Training',
                '==========================================',
                '| benchmark | batch | learning |         |',
                '| loss      | size  | rate     |   decay |',
                '------------------------------------------',
                '| %9.2f | %5i | %8.6f | %7.5f |' % (
                    self.benchmark(),
                    self.batch_size,
                    self.learning_rate,
                    self.decay,
                ),
                '==========================================\n\n'
            ])
        )
        
        serializer = lore.serializers.Keras(model=self)
        serializer.fitting += 1
        reload_best = ReloadBest(
            filepath=serializer.checkpoint_path,
            train=self.pipeline.encoded_training_data,
            validate=self.pipeline.encoded_validation_data,
            test=self.pipeline.encoded_test_data,
            benchmark_loss=self.benchmark(),
            monitor=self.monitor,
            mode='auto',
        )

        callbacks = self.callbacks()
        callbacks += [
            reload_best,
            TerminateOnNaN(),
            EarlyStopping(
                monitor=self.monitor,
                min_delta=min_delta,
                patience=patience,
                verbose=verbose,
                mode='auto',
            ),
        ]
        if tensorboard:
            callbacks += [TensorBoard(
                log_dir=serializer.tensorboard_path,
                histogram_freq=1,
                batch_size=self.batch_size,
                write_graph=True,
                write_grads=True,
                write_images=True,
                embeddings_freq=1,
                embeddings_metadata=None
            )]
     
        self.history = self.keras.fit(
            x=self.pipeline.encoded_training_data.x,
            y=self.pipeline.encoded_training_data.y,
            validation_data=(self.pipeline.encoded_validation_data.x, self.pipeline.encoded_validation_data.y),
            batch_size=self.batch_size,
            epochs=epochs,
            verbose=verbose,
            callbacks=callbacks
        )
        
        self.gain = reload_best.gain
        serializer.save(stats=reload_best.stats())
        return reload_best.stats()

    def predict(self, dataframe):
        encoded = self.pipeline.encode_x(dataframe)
        
        self._tf_graph_lock.acquire()
        try:
            with self._tf_graph.as_default():
                with timer('predict:'):
                    return self.keras.predict(encoded)
            return
        finally:
            self._tf_graph_lock.release()


class XGBoost(Base):
    def __init__(self):
        super(XGBoost, self).__init__()
        self.bst = None
        # http://xgboost.readthedocs.io/en/latest/parameter.html
        self.params = {}
    
    def fit(self):
        self.bst = xgboost.train(
            self.params,
            xgboost.DMatrix(pandas.DataFrame(self.pipeline.encoded_training_data.x), label=self.pipeline.encoded_training_data.y),
            num_boost_round=2
        )
        predictions = self.bst.predict(xgboost.DMatrix(pandas.DataFrame(self.pipeline.encoded_test_data.x)))
        mae = mean_absolute_error(
            predictions,
            self.pipeline.encoded_test_data.y,
        )
        return {
            'mae': mae
        }

    def predict(self, data):
        encoded = self.pipeline.encode(data, self.pipeline.input_encoders)
        with timer('predict:'):
            prediction = self.bst.predict(encoded)
        return self.decode(prediction)


class SKLearn(Base):
    def __init__(self):
        super(SKLearn, self).__init__()
        self.classifier = None
        
    def fit(self):
        self.classifier.fit(pandas.DataFrame(self.pipeline.encoded_training_data.x), self.pipeline.encoded_training_data.y)
        predictions = self.classifier.predict(pandas.DataFrame(self.pipeline.encoded_test_data.x))
        mae = mean_absolute_error(
            predictions,
            self.pipeline.encoded_test_data.y,
        )
        return {
            'mae': mae
        }
    
    def predict(self, data):
        encoded = self.encode(data)
        with timer('predict:'):
            prediction = self.classifier.predict(encoded)
        return self.decode(prediction)
