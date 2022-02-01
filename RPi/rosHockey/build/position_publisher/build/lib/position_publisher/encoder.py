import time
import spidev


class Encoder:

    def __init__(self, device) -> None:
        self.bus = 0
        self.device = device
        self.spi0 = spidev.SpiDev()
        self.spi0.open(self.bus, self.device)
        self.spi0.max_speed_hz = 500
        self.spi0.mode = 1
        self.angle = self.get_start_angle()

    def get_start_angle(self):
        done = False
        while (not done):
            data_read = self.spi0.readbytes(2)

            b1,b2 = bin(data_read[0])[2:], bin(data_read[1])[2:]
            if len(b1) == 8 and len(b2) == 8:
                b1 = b1[1:]
                b2 = b2[1:]
                done = True

        return int((b1+b2), 2)*360/2**13

    def get_angle(self):
        data_read = self.spi0.readbytes(2)

        b1,b2 = bin(data_read[0])[2:], bin(data_read[1])[2:]
        if len(b1) == 8 and len(b2) == 8:
            b1 = b1[1:]
            b2 = b2[1:]
            self.angle = int((b1+b2), 2)*360/2**13

        return self.angle

def main(args=None):
    e = Encoder(1)

    while("false"):
        print(e.get_angle())

if __name__ == '__main__':
    main()
