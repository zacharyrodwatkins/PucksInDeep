import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.layers import Layer, Dense
from tensorflow.keras import Sequential
import tensorflow.keras
from tensorflow.keras import Input
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt

class ModelLayer(Layer):

  def __init__(self, num_outputs):
      super(ModelLayer, self).__init__()
      self.num_outputs = num_outputs

  def build(self, input_shape):  # Create the state of the layer (weights)
    w_init = tf.random_normal_initializer()
    self.w = tf.Variable(
        initial_value=w_init(shape=(input_shape[-1], self.num_outputs),
                             dtype='float32'),
        trainable=True)

    # self.mask = tf.constant(([1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #                         [1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    #                         [1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    #                         [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    #                         [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
    #                         [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    #                         [1, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    #                         [1, 1, 1, 0, 0, 1, 1, 1, 0, 0],
    #                         [0, 1, 1, 1, 0, 0, 1, 1, 1, 0],
    #                         [0, 0, 1, 1, 1, 0, 0, 1, 1, 1]), dtype='float32')

  def call(self, inputs):  # Defines the computation from inputs to outputs
    # return tf.linalg.matvec(tf.math.multiply(self.mask, self.w), inputs)
    return tf.linalg.matvec(self.w, inputs)


model = Sequential([
    Input((10,)),
    ModelLayer(10)
])

# model = Sequential([
#     Input((10,)),
#     Dense(128, activation='relu'),
#     Dense(128, activation='relu'),
#     Dense(128, activation='relu'),
#     Dense(128, activation='relu'),
#     Dense(128, activation='relu'),
#     Dense(128, activation='linear'),
#     Dense(10)
# ])

def loss_func(real_volt, volt_pred):
    # print("real: ", real_volt.numpy())
    # print("pred: ", volt_pred.numpy())
    t = real_volt[:, -1]
    a = volt_pred[:,0] - real_volt[:,0]
    b = volt_pred[:,1] - real_volt[:,1]
    c = volt_pred[:,2] - real_volt[:,2]
    d = volt_pred[:,3] - real_volt[:,3]
    e = volt_pred[:,4] - real_volt[:,4]

    loss = e**2*t + d*e*t**2 + ((d**2 + 2*c*e)*t**3)/3 + ((c*d + b*e)*t**4)/2 + ((c**2 + 2*b*d + 2*a*e)*t**5)/5 + ((b*c + a*d)*t**6)/3 + ((b**2 + 2*a*c)*t**7)/7 + (a*b*t**8)/4 + (a**2*t**9)/9
    
    a = volt_pred[:,5] - real_volt[:,5]
    b = volt_pred[:,6] - real_volt[:,6]
    c = volt_pred[:,7] - real_volt[:,7]
    d = volt_pred[:,8] - real_volt[:,8]
    e = volt_pred[:,9] - real_volt[:,9]

    loss = loss + e**2*t + d*e*t**2 + ((d**2 + 2*c*e)*t**3)/3 + ((c*d + b*e)*t**4)/2 + ((c**2 + 2*b*d + 2*a*e)*t**5)/5 + ((b*c + a*d)*t**6)/3 + ((b**2 + 2*a*c)*t**7)/7 + (a*b*t**8)/4 + (a**2*t**9)/9
    loss = loss/t
    return loss


if __name__ == '__main__':
    model = tf.keras.models.load_model('physicalRefinedModel_mse_only.model', custom_objects={'ModelLayer': ModelLayer})
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss = 'mse') #, run_eagerly=True)

    print(model.summary())

    data_file = '/home/pham/PucksInDeep/RPi/rosHockey/data_logger/data/2022-03-23 18:44:15.907148refined_nn_data.pkl'


    with open(data_file, "rb") as f:
        theta,voltage = pkl.load(f)

    theta = theta
    print(theta.shape)
    print(voltage.shape)
    print(voltage[0])
    

    try:
        model.fit(theta, voltage[:,:-1], epochs = 4000000, batch_size = 4)

    except:
        print("exiting")
        pass
 
    print("saving")
    model.save("physicalRefinedModel_mse_only.model")
