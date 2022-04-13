import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.layers import Layer, Dense
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
    #   print("concatin")
    # time = inputs[:,-1]
    # print(tf.concat([tf.linalg.matvec(self.w,inputs[:,:-1]), time], axis=-1))
    # return tf.concat([tf.linalg.matvec(self.w,inputs[:,:-1]), time], axis=-1)
    return tf.linalg.matvec(self.w,inputs)

# model = Sequential([
#     Input((12,)),
#     ModelLayer()
# ])

model = Sequential([
    Input((12,)),
    Dense(128,activation = 'relu'),
    Dense(128,activation = 'relu'),
    Dense(128,activation = 'relu'),
    Dense(12,activation = 'linear')

])


# x = np.zeros(12)
# y = model(x)

def loss_func(real_volt, volt_pred):
    t = real_volt[:, -1]
    a = volt_pred[:,0] - real_volt[:,0]
    b = volt_pred[:,1] - real_volt[:,1]
    c = volt_pred[:,2] - real_volt[:,2]
    d = volt_pred[:,3] - real_volt[:,3]
    e = volt_pred[:,4] - real_volt[:,4]
    f = volt_pred[:,5] - real_volt[:,5]

    loss = a**2*t**11/11+t**9*(2*a*c+b**2)/9+t**7*(2*e*a+2*b*d+c**2)/7+t**6*(a*f+e*b+c*d)/3+t**8*(a*d+b*c)/4+a*b*t**10/5+t**5*(2*b*f+2*e*c+d**2)/5+t**4*(c*f+e*d)/2+t**3*(2*d*f+e**2)/3+f**2*t+e*f*t**2
    
    a = volt_pred[:,6] - real_volt[:,6]
    b = volt_pred[:,7] - real_volt[:,7]
    c = volt_pred[:,8] - real_volt[:,8]
    d = volt_pred[:,9] - real_volt[:,9]
    e = volt_pred[:,10] - real_volt[:,10]
    f = volt_pred[:,11] - real_volt[:,11]

    loss = loss + a**2*t**11/11+t**9*(2*a*c+b**2)/9+t**7*(2*e*a+2*b*d+c**2)/7+t**6*(a*f+e*b+c*d)/3+t**8*(a*d+b*c)/4+a*b*t**10/5+t**5*(2*b*f+2*e*c+d**2)/5+t**4*(c*f+e*d)/2+t**3*(2*d*f+e**2)/3+f**2*t+e*f*t**2
    loss = loss/t
    return loss


if __name__ == '__main__':
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4), loss = loss_func, run_eagerly=True)
    print(model.summary())

    data_file = '/home/pham/PucksInDeep/RPi/rosHockey/data_logger/data/2022-03-16 20 54 22.237820_nn_data_with_time.pkl'


    with open(data_file, "rb") as f:
        theta,voltage = pkl.load(f)

    print(voltage)
    try:
        model.fit(theta,voltage, epochs = 500, batch_size=4)
    except:
        pass
 
    model.save("realComplicatedModel1.model")
