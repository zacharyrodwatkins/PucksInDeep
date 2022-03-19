import tensorflow as tf
import tensorflow_probability as tfp
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
    #   print("concatin")
    #   print(tf.concat([tf.linalg.matvec(self.w,inputs), tf.constant([[0.0], [0.0], [0.0], [0.0]])], 1))
      return tf.linalg.matvec(self.w,inputs)

model = Sequential([
    Input((12,)),
    ModelLayer()
])

# x = np.zeros(12)
# y = model(x)

def loss_func(real_volt, volt_pred):
    loss = tf.zeros([0,4])
    time = tf.linspace(0.0, 0.2, 1000)

    t = 0.2 #real_volt[step, -1]
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
    # for step in range(volt_pred.shape[0]):
    #     loss1 = tfp.math.trapz((tf.math.polyval(list(volt_pred[step, 0:6].numpy()), time) - tf.math.polyval(list(real_volt[step, 0:6].numpy()), time))**2, time)
    #     loss2 = tfp.math.trapz((tf.math.polyval(list(volt_pred[step, 6:12].numpy()), time) - tf.math.polyval(list(real_volt[step, 6:12].numpy()), time))**2, time)

    #     step_loss = (loss1+loss2)/path_time
    #     print('loosin')
    #     loss = tf.concat([loss, tf.constant([step_loss])], 0)
        # pred = volt_pred[step]
        # real = real_volt[step]
        # next_loss = 0
        # path_time = real[-1]
        # print(path_time)
        # time = np.linspace(0, path_time, 1000)
        # for t in time:
        #     next_loss = next_loss + (poly(pred[0:6], t) - poly(real[0:6], t))**2 + (poly(pred[6:12], t) - poly(real[6:12], t))**2
        # next_loss = next_loss/path_time
        # loss.append(next_loss)

    return loss


if __name__ == '__main__':
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3), loss = loss_func, run_eagerly=True)
    print(model.summary())

    data_file = '/home/pham/PucksInDeep/RPi/rosHockey/data_logger/data/2022-03-16 20 54 22.237820_nn_data.pkl'


    with open(data_file, "rb") as f:
        theta,voltage = pkl.load(f)


    for volt in voltage:
        volt = np.append(volt, 0.2)
    model.fit(theta,voltage, epochs = 100, batch_size=4)
    model.save("realModel1.model")
