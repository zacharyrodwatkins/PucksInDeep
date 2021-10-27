import RPi.GPIO as GPIO
import time
m1 = 12
m2 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(m1,GPIO.OUT)
GPIO.setup(m2,GPIO.OUT)
GPIO.output(m1,GPIO.HIGH)
GPIO.output(m2,GPIO.HIGH)

while(True):
	time.sleep(2)
	GPIO.output(m1,GPIO.LOW)
	GPIO.output(m2,GPIO.LOW)
	time.sleep(2)
	GPIO.output(m1,GPIO.HIGH)
	GPIO.output(m2,GPIO.HIGH)

GPIO.cleanup()
