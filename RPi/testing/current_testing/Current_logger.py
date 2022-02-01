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


theta1 = []
theta2 = []
omega1 = []
omega2 = []
time_data = []
current_data = []

print("connecting to bluepill")
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
print("flushing serial")
ser.flush()
print("flushed")

send_val = 50
nbytes = ser.write(struct.pack('!B',send_val))
print("Sent motor speed: %d     number of bytes sent: %d" % (send_val, nbytes))

started = False
time_out = 0.5
path = 'Current_tests/26-01-2'
i = 1

def save_data(file_name, theta1, theta2, omega1, omega2, current_data, time_data):
    with open(file_name, "w") as f:
        f.write("speed={}\n".format(send_val))
        lines = ["{},{},{},{},{},{}\n".format(t1,t2,o1,o2,c,t) for t1,t2,o1,o2,c,t in zip(theta1, theta2, omega1, omega2, current_data, time_data)]
        f.writelines(lines)

last_read_time = inf

while (1):
    if (ser.in_waiting == 24):
        started = True
        last_read_time = time.time()
        data = ser.read(24)
        floats = struct.unpack('ffffff', data)
        print(floats)
        theta1.append(floats[0])
        theta2.append(floats[1])
        omega1.append(floats[2])
        omega2.append(floats[3])
        current_data.append(floats[4])
        time_data.append(floats[5])
        print("theta1: {} theta2: {} omega1: {} omega2: {} I: {}".format(*tuple(floats[:-1])))
    else:
        if time.time()-last_read_time>time_out and started == True:
            file_name = "run-{}.txt".format(i)
            save_data(file_name, theta1, theta2, omega1, omega2, current_data, time_data)
            theta1 = []
            theta2 = []
            omega1 = []
            omega2 = []
            current_data = []
            time_data = []
            started = False
            print("Done run {}".format(i))
            i += 1
            # nbytes = ser.write(struct.pack('!B',send_val))
            
            


    


# except KeyboardInterrupt:
#     print("done")
    
#     """
#     Saving Data File
#     """
#     date = datetime.now()
#     file_name = "current_testing-{}-{}-{}-{}".format(date.second, date.minute, date.hour, date.day, date.month)
#     with open("/home/ubuntu/PucksInDeep/RPi/ZN_test/Current_tests/"+file_name,'wb') as f:
#         pickle.dump([theta1,theta2,omega1,omega2,current_data,time_data],f)


#     """
#     Smoothing Current Data (recommended by ammeter manufacturer)
#     """
#     bin_size = 5
#     cur_avg_data = []
#     # for i in range(int(len(current_data)/bin_size)+1):
#     #     if (i+bin_size < len(current_data)):
#     #         avg = sum(current_data[i*bin_size:i*bin_size+bin_size])/bin_size
#     #         for j in range(5):
#     #             cur_avg_data.append(avg)
#     #     else:
#     #         last_bin_size = len(current_data) % bin_size
#     #         avg = sum(current_data[i*bin_size:])/last_bin_size
#     #         for j in range(last_bin_size):
#     #             cur_avg_data.append(avg)

#     for i in range(len(current_data)):
#         lower_bound = max([i - int(bin_size/2), 0])
#         upper_bound = min([i + int(bin_size/2), len(current_data) -1])
#         actual_bin_size = 1 + upper_bound - lower_bound
#         avg = sum(current_data[lower_bound:upper_bound+1])/float(actual_bin_size)
#         cur_avg_data.append(avg)


    

#     """
#     Plotting Data
#     """
#     fig, motor_ax = plt.subplots()
#     color = 'tab:red'
#     motor_ax.set_xlabel('time (ms)')
#     motor_ax.set_ylabel('motor angles (deg)', color=color)
#     motor_ax.plot(time_data, theta1, color='red')
#     motor_ax.plot(time_data, theta2, color='orange')
#     # plt.plot(time_data, omega1)
#     # plt.plot(time_data, omega2)
#     motor_ax.tick_params(axis='y', labelcolor=color)
    
#     current_ax = motor_ax.twinx()  # instantiate a second axes that shares the same x-axis
#     color = 'tab:blue'
#     current_ax.set_ylabel('current (A)', color=color)
#     current_ax.plot(time_data,current_data, color=color)
#     current_ax.plot(time_data,cur_avg_data, color='green')
#     current_ax.tick_params(axis='y', labelcolor=color)
   
#     # plt.legend(["theta1", "theta2", "current"])
#     plt.title("Current Test\nMotor Speeds: %d" % send_val)
#     plt.gcf().savefig("/home/ubuntu/PucksInDeep/RPi/ZN_test/Current_tests/"+file_name+"_fig.png")
#     plt.show()
    

#     # with open("logs/{}.pkl".format(datetime.now()), "wb") as f:
#     #     pkl.dump((theta1, theta2, omega1, omega2, time_data),f)
    

