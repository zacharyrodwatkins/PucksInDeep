from os import read
import serial
import time
import RPi.GPIO as GPIO
import numpy as np
import struct

from serial.serialutil import SerialException

global ser

def error_handler():
    while (1):
        print("Could not connect to BP on serial")
        time.sleep(0.1)

def connect_to_serial():
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
                error_handler()
        ser.flush()


def send_path(send_x, send_y):
    # Sends 40 bytes, 20 for desired x state, time and checksum, 20 for desired y state, time and checksum
    send_x.append(np.sum(send_x))
    ser.write(struct.pack('fffff', *send_x))
    print("sent x: ", send_x)
    send_y.append(np.sum(send_y))
    ser.write(struct.pack('fffff', *send_y))
    print("sent y: ", send_y)
    # print(ser.readline())
    # print(ser.readline())

    # while(1):
    #     # if ser.in_waiting >= 40:
    #     print(ser.read(40))
    

def send_pid(pid_x, pid_y):
    pid_x.append(np.sum(pid_x))
    ser.write(struct.pack('ffff', *pid_x))
    print("sent x: ", pid_x)
    pid_y.append(np.sum(pid_y))
    ser.write(struct.pack('ffff', *pid_y))
    print("sent y: ", pid_y)

def get_mallet_stat():
    floats = [0.0,0.0,0.0,0.0,0.0]
    if (ser.in_waiting >= 20):
        mallet_status = ser.read(20)
        try:
            for i in range(5):
                floats[i] = struct.unpack('f', mallet_status[4*i:4*i+4])[0]
        except struct.error:
            floats = np.zeros(5)
        # print("X: {} Y: {} Vx: {} Vy: {}".format(*tuple(floats[:-1])))
        # print("First Float: ", floats[0])
        # print("Second Float: ", floats[1])
        # print("Third Float: ", floats[2])
        # print("Fourth Float: ", floats[3])
        # print("Sum: ", floats[4])
        # print(floats)
        # ser.flush()
        return floats
    else:
        # print("no mallet status data")
        return -1

# def test_1():
#     y = 0
#     last_send_time = 0
#     while(True):
#         mallet_stat = get_mallet_stat()
#         if mallet_stat != -1:
#             print("mal stat")
#             print(mallet_stat)
        
    
#         t = time.time()
#         # print(ser.in_waiting)
#         if t - last_send_time > 5:
#             # print(ser.in_waiting)
#             send_path([30.0,0.0,0,0.5],[y,0,0,0.5])
#             time.sleep(0.1)
#             print(ser.readline())
#             print(ser.readline())
#             # print("5 secs")
#             last_send_time = t
#             y += 10
# if __name__ == "__main__":
#     test_1()
    