from matplotlib import ticker
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.twodim_base import vander

from cmath import inf
import numpy as np
import matplotlib.pyplot as plt
import serial
import struct
import time
import sys
import pickle as pkl
from serial.serialutil import SerialException
from datetime import datetime
from scipy.fft import fft, fftfreq
import pickle

from os import read
import serial
import time
import RPi.GPIO as GPIO
import numpy as np
import struct





def get_coeffs(start, stop, Dt):
    mat = gen_mat(Dt)
    s = np.zeros(6)
    s[:3] = start 
    s[3:] = stop
    return np.linalg.solve(mat,s)


def gen_mat(Dt):
    T= np.vander(np.array([Dt]),6)[0]
    mat = np.zeros((6,6))
    mat[:3,3:] = np.array([[0,0,1],[0,1,0],[2,0,0]])
    mat[3] = T
    mat[4,:-1] = np.array([5,4,3,2,1])*T[1:]+np.array([0,0,0,0,1])
    mat[5,:-2] = T[2:]*np.array([20,12,6,0]) + np.array([0,0,0,2])
    return mat


ti = 1
xstart = np.array([0,0,0])
xend = [400,0,0]
ystart = np.array([0,0,0])
yend = [400,0,0]

xcoeffs = get_coeffs(xstart,np.array(xend), 1)
ycoeffs = get_coeffs(ystart,np.array(yend), 1)
t = np.linspace(0,ti)
# t = vander(t,6).shape
# print(t)
x = np.matmul(vander(t,6),xcoeffs)
y = np.matmul(vander(t,6),ycoeffs)
# plt.plot(t,y)
# plt.show()



print("connecting to bluepill")
try:
    ser1 = serial.Serial('/dev/ttyUSB0',1000000, timeout=0.01)
    print("CONNECTED TO USB0\n--------------------------")
except SerialException:
    try :
        ser1 = serial.Serial('/dev/ttyUSB1',1000000, timeout=0.01)
        print("CONNECTED TO USB1\n--------------------------")
    except SerialException:
        try :
            ser1 = serial.Serial('/dev/ttyUSB2',1000000, timeout=0.01)
            print("CONNECTED TO USB2\n--------------------------")
        except SerialException:
            print("uh oh spagettio")
            quit()
print("flushing serial")
ser1.flush()
print("flushed")



cs_pin = 16
err_pin = 12
ser = serial.Serial('/dev/ttyUSB0',1000000, timeout=0.01)
ser.flush()

floats = [0,0,0,0,0]
correct = 0
bp_success = 0
writetime = 0
total_write = 0
total_read = 0
readtime = 0
w_max = 0
r_max = 0
total = 0


def send_path(send_x, send_y):
    # Sends 40 bytes, 20 for desired x state, time and checksum, 20 for desired y state, time and checksum
    send_x.append(np.sum(send_x))
    ser.write(struct.pack('fffff', *send_x))
    send_y.append(np.sum(send_y))
    ser.write(struct.pack('fffff', *send_y))

xend.append(ti)
yend.append(ti)
send_path(xend,yend)


X = []
Y = []
VX = []
VY = []
time_data = []



started = False
time_out = 0.5
path = '2022-02-02'
i = 1

def save_data(file_name, theta1, theta2, omega1, omega2, current_data, time_data):
    with open(file_name, "w") as f:
        lines = ["{},{},{},{},{},{}\n".format(t1,t2,o1,o2,c,t) for t1,t2,o1,o2,c,t in zip(theta1, theta2, omega1, omega2, current_data, time_data)]
        f.writelines(lines)
    
def save_data_XY(file_name,xcoefs,ycoefs, X, Y, VX, VY, time_data):
    with open(file_name, "w") as f:
        line1 = ["{},{},{},{},{},{},{},{},{},{},{},{}\n".format(xcoefs[0],xcoefs[1],xcoefs[2],xcoefs[3],xcoefs[4],xcoefs[5],ycoefs[0],ycoefs[1],ycoefs[2],ycoefs[3],ycoefs[4],ycoefs[5])]
        line2 = ["{},{},{},{},{}\n".format(t1,t2,o1,o2,t) for t1,t2,o1,o2,t in zip(X, Y, VX, VY, time_data)]
        f.writelines(line1)
        f.writelines(line2)

last_read_time = inf

while (1):
    if (ser1.in_waiting == 20):
        started = True
        last_read_time = time.time()
        data = ser1.read(20)
        floats = struct.unpack('fffff', data)
        print(floats)
        # theta1.append(floats[0])
        # theta2.append(floats[1])
        # omega1.append(floats[2])
        # omega2.append(floats[3])
        # current_data.append(floats[4])
        # time_data.append(floats[5])
        X.append(floats[0])
        Y.append(floats[1])
        VX.append(floats[2])
        VY.append(floats[3])
        time_data.append(floats[4])
        # print("theta1: {} theta2: {} voltage1: {} voltage2: {} I: {}".format(*tuple(floats[:-1])))
        print("X: {} Y: {} VX: {} VY: {}".format(*tuple(floats[:-1])))
    else:
        if time.time()-last_read_time>time_out and started == True:
            file_name = path + "/run-{}.txt".format(i)
            # save_data(file_name, theta1, theta2, omega1, omega2, current_data, time_data)
            save_data_XY(file_name, xcoeffs,ycoeffs, X, Y, VX, VY, time_data)
            # theta1 = []
            # theta2 = []
            # omega1 = []
            # omega2 = []
            # current_data = []
            # time_data = []
            X = []
            Y = []
            VX = []
            VY = []
            time_data = []
            started = False
            print("Done run {}".format(i))
            i += 1

