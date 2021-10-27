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
                print("motor1 up")

                return 1
        elif k=='\x1b[B':
                print("motor2 down")
                return -1
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
 
def setup():
    global pwm
    global pwm2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin1, GPIO.OUT)
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.setup(motor_pin2, GPIO.OUT)
    GPIO.output(motor_pin2, GPIO.LOW)
    pwm = GPIO.PWM(motor_pin1, 5000)
    pwm2 = GPIO.PWM(motor_pin2,5000)
    pwm.start(0)
    pwm2.start(0)

def loop():
    dc = 50
    dc2 = 50
    while True:
        pwm.ChangeDutyCycle(dc)
        # pwm.ChangeDutyCycle(50)
        pwm2.ChangeDutyCycle(dc2)
        # pwm2.ChangeDutyCycle(70)
        # continue
        time.sleep(0.01)
        got = get()
        if got == "quit":
            return 
        dc = dc + 10*got
        if mode == 'f':
            dc2 = 100 - dc
        else:
            dc2 = dc
        dc = min(dc, 100)
        dc = max(dc, 0)
        dc2 = min(dc2, 100)
        dc2 = max(dc2, 0)
        print(dc,dc2)
         
def destroy():
    pwm.stop()
    GPIO.output(motor_pin1, GPIO.LOW)
    GPIO.cleanup()
     
if  __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print("here1")
        destroy()
        print("here")
        quit()
    destroy()
    quit()
