import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras import Sequential
from tensorflow.keras import Input
import numpy as np
import pickle as pkl

class ModelLayer(Layer):

  def __init__(self, name=None, **kwargs):
      super(ModelLayer, self).__init__()

  def build(self, input_shape):  # Create the state of the layer (weights)
    w_init = tf.random_normal_initializer()
    self.w = tf.Variable(
        initial_value=w_init(shape=(input_shape[-1], input_shape[-1]),
                             dtype='float32'),
        trainable=True)

  def call(self, inputs):  # Defines the computation from inputs to outputs
      return tf.linalg.matvec(self.w,inputs)

model = Sequential([
    Input((12,)),
    ModelLayer()
])

# x = np.zeros(12)
# y = model(x)


if __name__ == '__main__':
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss ='mse')
    print(model.summary())

    data_file = '../RPi/rosHockey/data_logger/data/2022-03-16 20:54:22.237820_nn_data.pkl'


    with open(data_file, "rb") as f:
        theta,voltage = pkl.load(f)


    model.fit(theta,voltage, epochs = 100000)
    model.save("realModel1.model")
