from __future__ import division, print_function, absolute_import
import tefla
import logging
from tefla.core.learning import SupervisedLearner
from tefla.core.lr_policy import StepDecayPolicy
from tefla.core.layers import fully_connected as fc, relu, input, softmax
from tefla.core.special_layers import embedding
from tefla.core.layer_arg_ops import common_layer_args, make_args, end_points
from tefla.core.rnn_cell import LSTMCell, lstm
from tefla.core.mem_dataset import DataSet
from tefla.utils.util import pad_sequences
from tefla.utils import util
from examples.datasets import imdb

import tensorflow as tf
import numpy as np


def model(x, is_training, reuse):
    common_args = common_layer_args(is_training, reuse)
    fc_args = make_args(activation=relu, **common_args)
    logit_args = make_args(activation=None, **common_args)
    # x = input((None, 100), **common_args)
    x = embedding(x, 10000, 128, reuse)
    """
    sequence_length = util.retrieve_seq_length(x)
    if type(x) not in [list, np.array]:
        ndim = len(util.get_input_shape(x))
        assert ndim >= 3, "Input dim should be at least 3."
        axes = [1, 0] + list(range(2, ndim))
        x = tf.transpose(x, (axes))
        x = tf.unstack(x)
    cell = LSTMCell(34, reuse)
    x, _ = tf.contrib.rnn.static_rnn(cell, x, dtype=tf.float32)
    x = tf.transpose(tf.stack(x), [1, 0, 2])
    x = util.advanced_indexing(x, sequence_length)
    # x = tf.gather(x, int(x.get_shape()[0]) - 1)
    """
    x = lstm(x, 34, reuse, is_training)
    logits = fc(x, 2, name='logits', **logit_args)

    predictions = softmax(logits, name='predictions', **common_args)
    return end_points(is_training)


def main():
    train, test, _ = imdb.load_data(path='imdb.pkl', n_words=10000,
                                    valid_portion=0.1)
    trainX, trainY = train
    testX, testY = test

    trainX = pad_sequences(trainX, maxlen=100, value=0.)
    testX = pad_sequences(testX, maxlen=100, value=0.)
    trainY = np.asarray(trainY)
    testY = np.asarray(testY)
    data_set = DataSet(trainX, trainY,
                       testX, testY)
    training_cnf = {
        'classification': True,
        'validation_scores': [('validation accuracy', util.accuracy_tf)],
        'num_epochs': 50,
        'input_size': (100, ),
        'lr_policy': StepDecayPolicy(
            schedule={
                0: 0.01,
                30: 0.001,
            }
        )
    }
    util.init_logging('train.log', file_log_level=logging.INFO,
                      console_log_level=logging.INFO)

    learner = SupervisedLearner(
        model, training_cnf, classification=training_cnf['classification'], is_summary=False)
    learner.fit(data_set, weights_from=None,
                start_epoch=1)


if __name__ == '__main__':
    main()
