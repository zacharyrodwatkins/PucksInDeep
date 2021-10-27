# spitest.py
# A brief demonstration of the Raspberry Pi SPI interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun Serial 7 Segment display:
# https://www.sparkfun.com/products/11629

import time
import spidev

TICKS_TO_DEG = 360.0/(2**13)

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
Left_device = 1
Right_device = 0

# Enable SPI
spi_Left = spidev.SpiDev()
spi_Right = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi_Left.open(bus, Left_device)
spi_Right.open(bus,Right_device)

# Set SPI speed and mode
spi_Left.max_speed_hz = int(9e6)
spi_Left.mode = 1
spi_Right.max_speed_hz = int(9e6)
spi_Right.mode = 1
# spi.bits_per_word = 11

pos_history = [(1,1), (1,1), (1,1), (1,1), (1,1)]
cur_pos_Left = 0
cur_pos_Right = 0
speed = 0
while (1):
    # spi.writebytes([0b11111111,0b10111111])
    data_read_Left = spi_Left.readbytes(2)
    data_read_Right = spi_Right.readbytes(2)
    # print(data_read)
    # print(spi0.xfer([0b00111111,0b11111111]))
    # print(data_read)
    # time.sleep(0.5)
    Lb1,Lb2 = bin(data_read_Left[0])[2:], bin(data_read_Left[1])[2:]
    Rb1,Rb2 = bin(data_read_Right[0])[2:], bin(data_read_Right[1])[2:]
    if len(Lb1) == 8 and len(Lb2) == 8:
        # print(b1+b2)
        # time_stamp = time.time()
        Lb1 = Lb1[1:]
        Lb2 = Lb2[1:]
        # print(b1+b2)
        # print(int(b1+b2, 2))
        # print(int((b1+b2)[0:11], 2))
        # print(int((b1+b2)[0:14], 2))
        cur_pos_Left = int((Lb1+Lb2), 2)*TICKS_TO_DEG
        # pos_history.pop()
        # pos_history.insert(0, (cur_pos_Left, time_stamp))
        # try:
        #     # print(pos_history[0:2])
        #     # print(cur_pos)
        #     # print("angle change: " + str((float(pos_history[0][0]) - float(pos_history[1][0]))))
        #     # print("time change: " + str((float(pos_history[0][1]) - float(pos_history[1][1]))))
        #     speed = (float(pos_history[0][0]) - float(pos_history[1][0]))/(float(pos_history[0][1]) - float(pos_history[1][1]))/360*60
        # except ZeroDivisionError:
        #     print(":(")
        # print("speed: {}".format(speed))
    print("Left Motor Current Position = {}".format(cur_pos_Left))

    if len(Rb1) == 8 and len(Rb2) == 8:
        Rb1 = Rb1[1:]
        Rb2 = Rb2[1:]
        cur_pos_Right = int((Rb1+Rb2), 2)*TICKS_TO_DEG
    print("Right Motor Current Position = {}".format(cur_pos_Right))
    # print(b1,b2)
    # print("Time elapsed : {}".format(t1-t0))
    # print(len(b1),len(b2))
    # time.sleep(0.5)



