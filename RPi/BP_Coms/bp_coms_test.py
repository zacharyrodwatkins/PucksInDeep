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
GPIO.setmode(GPIO.BCM) # uses GPIO numbering
GPIO.setup(cs_pin, GPIO.OUT)
GPIO.setup(err_pin, GPIO.IN)
# send = [100*int(i) for i in np.random.random(12)] #3 floats (12 bytes)
send = [1.01, 6.9, 4.20, 69.0, 1.01+6.9+4.20+69.0]
# send = [1,2,3]
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

while True:
    send = [100*float(x) for x in np.random.random(4)]
    send.append(np.sum(send))
    # send = [x+1 for x in send]
    # send[4] += 3

    print(send)
    # print(struct.pack('fffff', *send))
    # start = time.time()
    # ser.flush()
    ser.write(struct.pack('fffff', *send))
    # ser.write(send)
    # ser.write(b"\n")
    # # writetime = time.time()-start
    # ser.flush()
    # start = time.time()
    rec = ser.read(20)
    # readtime = time.time()-start

    writetime = int(ser.readline())
    readtime = int(ser.readline())
    bp_success += int(ser.readline())

    # print(rec)
    for i in range(5):
        floats[i] = struct.unpack('f', rec[4*i:4*i+4])[0]
    print(floats)
    # print("First Float: ", floats[0])
    # print("Second Float: ", floats[1])
    # print("Third Float: ", floats[2])
    # print("Fourth Float: ", floats[3])
    # print("Sum: ", floats[4])
    checksum = np.sum(floats[0:4])
    if (abs(checksum - send[4]) < 0.001):
        correct += 1

    total_write += writetime
    total_read += readtime
    total += 1
    w_max = max(w_max, writetime)
    r_max = max(r_max, readtime)
    print("avg write: ", total_write/total)
    print("avg read: ", total_read/total)
    print("max write: ", w_max)
    print("max read: ", r_max)

    print("success rate: ", correct/total)
    print("bp success rate: ", bp_success/total)
    time.sleep(0.01)