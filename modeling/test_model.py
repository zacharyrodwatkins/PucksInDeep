import tensorflow as tf
import numpy as np
import pickle as pkl
from train_model import ModelLayer
import matplotlib.pyplot as plt

model = tf.keras.models.load_model('nonPhysical1.model', custom_objects={'ModelLayer': ModelLayer})
ThetaLeft = [-7.59549467,  4.45860237, 10.52031479,  9.94941655, -1.27084973, -1.43242888]     
ThetaRight = [13.34909161, 24.33989879, -0.8963008,  -4.59193911, 24.27809849, -2.04917566]
VoltageLeft = [ 0, -3.63600588,  0.1319521 ,  2.06339679,  2.31830621 , 0.15726169]
VoltageRight = [ 0, 6.6163691,  12.27394173 , 2.44819776, -0.76413693 , 2.28754383]

data_file = '../RPi/rosHockey/data_logger/data/2022-03-16 20:54:22.237820_nn_data.pkl'
with open(data_file, "rb") as f:
    theta, v = pkl.load(f)


v_pred = model.predict(theta)

t = np.linspace(0,0.2)
# V_pred_1 = np.polyval(v_pred[0:6], t)
# V_pred_2 = np.polyval(v_pred[6:], t)
# theta_1 = np.polyval(theta[0,0:6], t)
# theta_2 = np.polyval(theta[0,6:], t)
# V_act_1 = np.polyval(v[0,0:6], t)
# V_act_2 = np.polyval(v[0,6:], t)
labels = ['theta 1','theta 2', 'V1', 'V2', 'V1 pred', 'V2 pred']

for i in range(len(theta)):
    print(theta[i,0:6], theta[i,6:], v[i,0:6],v[i,6:])
    theta_1 = np.polyval(theta[i,0:6], t)
    theta_2 = np.polyval(theta[i,6:], t)
    V_act_1 = np.polyval(v[i,0:6], t)
    V_act_2 = np.polyval(v[i,6:], t)
    V_pred_1 = np.polyval(v_pred[i,0:6], t)
    V_pred_2 = np.polyval(v_pred[i,6:], t)
    for i,thang in enumerate([theta_1, theta_2, V_act_1, V_act_2, V_pred_1, V_pred_2]):
        plt.plot(t,thang, label = labels[i])
    plt.legend()
    plt.show()

# for thang in [V_pred_1, V_pred_2, theta_1, theta_2, V_act_1, V_act_2]:
#     plt.plot(t,thang)

# plt.legend(["V1 pred", "V2 pred", "theta 1", "theta 2", "V1 act", "V2 act"])
plt.show()