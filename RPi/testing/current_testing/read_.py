from time import sleep
import RPi.GPIO as GPIO
from datetime import datetime

# Set up BCM GPIO numbering.
GPIO.setmode(GPIO.BCM)
# Set up input pins.
SENSOR_1_INPUT = 22
SENSOR_2_INPUT = 23
GPIO.setup(SENSOR_1_INPUT, GPIO.IN)
GPIO.setup(SENSOR_2_INPUT, GPIO.IN)

current_values = []

AMPS_PER_V = 1/(12/1000) 

# Initiate the loop.


while True:
    # Get signals from Arduino as digital input values.
    try:
        while True:
            SENSOR_1_VALUE = GPIO.input(SENSOR_1_INPUT)
            SENSOR_2_VALUE = GPIO.input(SENSOR_2_INPUT)
            current_values.append((SENSOR_1_VALUE-SENSOR_2_VALUE)*AMPS_PER_V)
    except KeyboardInterrupt:
        break

        

date = datetime.now()
file_name = "current_testing-{}-{}-{}-{}".format(date.minute, date.hour, date.day, date.month)

with open(file_name, 'w') as f:
    f.writelines(current_values)


