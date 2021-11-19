from os import read
import serial
import time
import RPi.GPIO as GPIO
import numpy as np
import struct

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
    
def get_mallet_stat():
    if (ser.in_waiting == 20):
        mallet_status = ser.read(20)
        try:
            for i in range(5):
                floats[i] = struct.unpack('f', mallet_status[4*i:4*i+4])[0]
        except struct.error:
            floats = np.zeros(5)
        print(floats)
        # print("First Float: ", floats[0])
        # print("Second Float: ", floats[1])
        # print("Third Float: ", floats[2])
        # print("Fourth Float: ", floats[3])
        # print("Sum: ", floats[4])
        return floats
    else:
        print("no mallet status data")
        return -1
