import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import Sequential



class ModelLayer(Layer):

  def __init__(self):
      super(ModelLayer, self).__init__()

  def build(self, input_shape):  # Create the state of the layer (weights)
    w_init = tf.random_normal_initializer()
    self.w = tf.Variable(
        initial_value=w_init(shape=(input_shape[-1], input_shape[-1]),
                             dtype='float32'),
        trainable=True)

  def call(self, inputs):  # Defines the computation from inputs to outputs
      return tf.matmul(inputs, self.w)

model =

