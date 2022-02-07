import time
import spidev
TICKS_TO_DEG = 360/2**14
two_to_the_8 = 2**8 

class Encoder:

    def __init__(self, device) -> None:
        self.bus = 0
        self.device = device
        self.spi0 = spidev.SpiDev()
        self.spi0.open(self.bus, self.device)
        self.spi0.max_speed_hz = int(2e6)
        self.spi0.mode = 1
        self.get_angle()


    def get_angle(self):    
        data_read_Right = self.spi0.readbytes(2)

        Rb1,Rb2 = bin(data_read_Right[0]), bin(data_read_Right[1])
        num1s = Rb1.count("1")+ Rb2.count("1")

        if num1s % 2 == 0 and int(int(Rb1[2:]) / two_to_the_8):
            if len(Rb1) == 10: 
                Rb1 = Rb1[4:]
            else:
                Rb1 = Rb1[2:]

            Rb2 = Rb2[2:]
            if len(Rb2)<8:
                Rb2 = "0"*(8-len(Rb2)) + Rb2
            self.angle = int(Rb1+Rb2,2)*TICKS_TO_DEG
            return self.angle
            

    def get_start_angle(self):
        return self.get_angle()
        # done = False
        # while (not done):
        #     data_read = self.spi0.readbytes(2)

        #     b1,b2 = bin(data_read[0])[2:], bin(data_read[1])[2:]
        #     if len(b1) == 8 and len(b2) == 8:
        #         b1 = b1[1:]
        #         b2 = b2[1:]
        #         done = True

        # return int((b1+b2), 2)*360/2**13

    # def get_angle(self):
    #     data_read = self.spi0.readbytes(2)

    #     b1,b2 = bin(data_read[0])[2:], bin(data_read[1])[2:]

    #     if len(b1) == 8 and len(b2) == 8:
    #         b1 = b1[1:]
    #         b2 = b2[1:]
    #         self.angle = int((b1+b2), 2)*360/2**13
    #     else:
    #         print("Dropped. Length:{} {}".format(len(b1),len(b2)))

    #     return self.angle

def main(args=None):
    e = Encoder(1)

    while("false"):
        print(e.get_angle())

if __name__ == '__main__':
    main()
