import serial
from serial.serialutil import SerialException
import time
import struct
import numpy as np
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import NextPath


class bp_tx(Node):

    def __init__(self):
        super().__init__('bp_tx')
        self.nextpath_subscription = self.create_subscription(NextPath, 'PATH', self.send_next_path, 10)
        self.ser = None
        for i in range(3):
            try:
                self.ser = serial.Serial('/dev/ttyUSB{}'.format(i),1000000, timeout=0.01)
                break
            except SerialException:
                pass
        if self.ser == None:
            raise SerialException("Could not connect to bluepill")

            
    def send_next_path(self, NextPath):
        x_params = (NextPath.x, NextPath.vx, NextPath.ax, NextPath.t)
        y_params = (NextPath.y, NextPath.vy, NextPath.ay, NextPath.t)
        msg_x = (*x_params, sum(x_params))
        msg_y = (*y_params, sum(y_params))
        print (msg_x, msg_y)
        self.ser.write(struct.pack('ffffffffff', *msg_x, *msg_y))
    

    
def main(args=None):
    rclpy.init(args=args)
    tx = bp_tx()
    rclpy.spin(tx)

    tx.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()