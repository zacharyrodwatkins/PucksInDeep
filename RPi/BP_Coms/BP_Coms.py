from os import read
import serial
import time
import RPi.GPIO as GPIO
import numpy as np
import struct

cs_pin = 16
err_pin = 12
ser = serial.Serial('/dev/ttyUSB0',1000000, timeout=1)
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

def send_path_get_mallet_stat(send):
    send.append(np.sum(send))
    ser.write(struct.pack('fffff', *send))
    mallet_status = ser.read(20)
    for i in range(5):
        floats[i] = struct.unpack('f', mallet_status[4*i:4*i+4])[0]
    print(floats)
    # print("First Float: ", floats[0])
    # print("Second Float: ", floats[1])
    # print("Third Float: ", floats[2])
    # print("Fourth Float: ", floats[3])
    # print("Sum: ", floats[4])
    return floats
