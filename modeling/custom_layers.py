import tensorflow as tf
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import Sequential
from tensorflow.keras import Input
import numpy as np
import pickle as pkl

class DitchLastArg(Layer):

  def __init__(self, name=None, **kwargs):
      super(DitchLastArg, self).__init__()

  def build(self, input_shape):  # Create the state of the layer (weights)
    return

  def call(self, inputs):  # Defines the computation from inputs to outputs
      return inputs[:-1]

# x = np.array([1,2,3,4])
# l = DitchLastArg()

# y = l(x)
# print(y)


