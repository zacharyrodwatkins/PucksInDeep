import RPi.GPIO as GPIO
import time
import sys,tty,termios
global mode
mode = "f"

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k=='\x1b[A':
            return "up"
        elif k=='\x1b[B':
            return "down"
        elif k=='\x1b[D':
            return "left"
        elif k=='\x1b[C':
            return "right"       
        elif 'q' in k:
            return "quit"
        return 0
 
# def get2():
#     inkey = _Getch()
#     while(1):
#         k=inkey()

motor_pin1 = 12
motor_pin2 = 13 

# analog control constants for motors
MAX_VOLTAGE = 2 # volts
MIN_VOLTAGE = 0
NO_SPEED_VOLTAGE = (MAX_VOLTAGE + MIN_VOLTAGE)/2

from roboclaw_3 import Roboclaw
from time import sleep
address1 = 0x80
address2 = 0x81
roboclaw = Roboclaw("/dev/ttyAMA0", 2400)
roboclaw.Open()
fact = 4

	

def loop():
    m1 = 0
    m2 = 0
    mode = "fb"
    while True:
        time.sleep(0.01)
        got = get()
        if got == "quit":
            return 
        
        if got == "up" or got == "down":
            if mode == 'fb':
                inc = (1 if got == "up" else -1)*fact
                m1 += inc
                m2 += -inc 
            elif mode == 'ss':
                mode = 'fb'
                m1 = m2 = 0
            
        if got == "left" or got == "right":
            if mode == 'ss':
                inc = (1 if got == "right" else -1)*fact
                m1 += inc
                m2 += inc 
            elif mode == 'fb':
                mode = 'ss'
                m1 = m2 = 0


        m1 = min(m1, 128)
        m1 = max(m1, -128)
        m2 = min(m2, 128)
        m2 = max(m2, -128)

        if m1 > 0:
            roboclaw.ForwardM1(address1,m1)
            print("Forward {}".format(m1))
        else:
            roboclaw.BackwardM1(address1,-m1)
            print("Backwards {}".format(-m1))
        
        if m2 > 0:
            roboclaw.ForwardM1(address2,m2)
        else:
        	roboclaw.BackwardM1(address2,-m2)
        	       

        print(mode,m1,m2)
         
if  __name__ == '__main__':
    loop()
