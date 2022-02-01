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

def send_pid(pid_x, pid_y):
    pid_x.append(np.sum(pid_x))
    ser.write(struct.pack('ffff', *pid_x))
    print("sent pid x: ", pid_x)
    pid_y.append(np.sum(pid_y))
    ser.write(struct.pack('ffff', *pid_y))
    print("sent pid y: ", pid_y)

x_data = []
y_data = []
xvel_data = []
yvel_data = []
time_data = []
# time_start = time.time()

            

# pid_vals = sys.argv[1:]
# pid_vals = np.array(pid_vals).astype(float)

# pid_x = [0,0,0]
# pid_y = [0,0,0]

# if len(pid_vals)==4:
#     pid_x[0] = pid_vals[0]
#     pid_x[-1] = pid_vals[1]
#     pid_y[0] = pid_vals[2]
#     pid_y[-1] = pid_vals[3]

# elif len(pid_vals==6):
#     pid_x = list(pid_vals[0:3])
#     pid_y = list(pid_vals[3:])

# else:
#     print("Enter either PD or PID for both X and Y")
#     quit()

try:
    ser = serial.Serial('/dev/ttyUSB0',1000000, timeout=0.01)
    print("CONNECTED TO USB0\n--------------------------")
except SerialException:
    try :
        ser = serial.Serial('/dev/ttyUSB1',1000000, timeout=0.01)
        print("CONNECTED TO USB1\n--------------------------")
    except SerialException:
        try :
            ser = serial.Serial('/dev/ttyUSB2',1000000, timeout=0.01)
            print("CONNECTED TO USB2\n--------------------------")
        except SerialException:
            print("uh oh spagettio")
            quit()

# send_pid(pid_x,pid_y)

try:
    while (1):
        if (ser.in_waiting == 20):
            # time_now = time.time()-time_start
            data = ser.read(20)
            floats = struct.unpack('fffff', data)
            print(floats)
            x_data.append(floats[0])
            y_data.append(floats[1])
            xvel_data.append(floats[2])
            yvel_data.append(floats[3])
            time_data.append(floats[4])
            # time_data.append(floats[4])
            # time_data.append(time_now)
            # print("X: {} Y: {} Vx: {} Vy: {}".format(*tuple(floats[:-1])))
            # print("First Float: ", floats[0])
            # print("Second Float: ", floats[1])
            # print("Third Float: ", floats[2])
            # print("Fourth Float: ", floats[3])
            # print("Sum: ", floats[4])
            # ser.flush()

except KeyboardInterrupt:
    print("done")
    time_data = np.array(time_data) - time_data[0]
    # time_data_start_index = np.where(np.array(y_data) > 0.5)[0][0]
    # time_data = time_data[time_data_start_index:]
    # y_data = y_data[time_data_start_index:]
    with open("/home/ubuntu/PucksInDeep/RPi/ZN_test/MotorEfforts_Testread",'wb') as f:
        pickle.dump([x_data,y_data,xvel_data,yvel_data,time_data],f)
    plt.figure()
    plt.plot(time_data, x_data)
    plt.plot(time_data, y_data)
    plt.plot(time_data, xvel_data)
    plt.plot(time_data, yvel_data)
    plt.legend(["x", "y", "x vel", "y vel"])
    plt.title("Motor efforts 110")
    plt.gcf().savefig("/home/ubuntu/PucksInDeep/RPi/ZN_test/MotorEfforts_Testread_fig.png")
    plt.show()
    
    # N = len(time_data)
    # T = np.mean(time_data[1:]-time_data[0:-1])

    # yf = fft(y_data)
    # xf = fftfreq(N, T)[:N//2]

    # plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))

    # plt.grid()

    # plt.show()


    # with open("logs/{}.pkl".format(datetime.now()), "wb") as f:
    #     pkl.dump((x_data, y_data, xvel_data, yvel_data, time_data),f)
    

