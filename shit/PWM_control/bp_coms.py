import serial
import time

if __name__ == "__main__":
    
    ser = serial.Serial("/dev/ttyAMA0", 9600)
    ser.open()
    while True:
        print("loopin\n")
        ser.write(16)
        print(ser.read())
        # time.sleep(1)
    
