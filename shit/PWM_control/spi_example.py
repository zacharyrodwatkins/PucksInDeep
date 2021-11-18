# spitest.py
# A brief demonstration of the Raspberry Pi SPI interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun Serial 7 Segment display:
# https://www.sparkfun.com/products/11629

import time
import spidev
import numpy as np
import RPi.GPIO as GPIO

# SPI bus 0
bus = 0

# Chip select pin
cs_bp = 8

# Enable SPI
spi_bp = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi_bp.open(bus, 0)
# spi_bp.no_cs = True

# Set SPI speed and mode
max_speed_order = 5
spi_bp.max_speed_hz = int(10**max_speed_order)
spi_bp.mode = 0
poly_coefs = [1, 2, 3, 4, 5, 6]
count = 0
success = 0

try:
    while (1):
        start = time.time()
        # print("\nSPI TRANSATION:")
        # print("sending: ")
        # if (count%2):
        #     send = poly_coefs
        # else:
        #     send = [69, 69, 69, 69, 69, 69]
        send = list(int(x) for x in 100*np.random.random(6))
        print(send)

        spi_bp.writebytes(send)
        # print("received: ")
        receive = spi_bp.readbytes(6)
        print(receive)
        print(time.time() - start)
        count += 1
        if (send == receive):
            success += 1
        
        print(float(success)/count)
        time.sleep(0.01)

except KeyboardInterrupt:
    print("closing\n")

finally:
    GPIO.cleanup()

