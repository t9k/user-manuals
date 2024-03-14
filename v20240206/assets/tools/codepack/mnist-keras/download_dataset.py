import os
import tensorflow as tf

_, _ = tf.keras.datasets.mnist.load_data(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mnist.npz'))
