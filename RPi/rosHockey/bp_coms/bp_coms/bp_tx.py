from os import read
from xmlrpc.client import Server
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
                self.ser.flush()
                break
            except SerialException:
                pass
        if self.ser == None:
            raise SerialException("Could not connect to bluepill")

            
    def send_next_path(self, NextPath):
        self.bp_msg.extend[(NextPath.x, NextPath.y, NextPath.vx, NextPath.vy, NextPath.ax, NextPath.ay, NextPath.t)]
        self.ser.write(struct.pack('fffffff', *self.bp_msg))
    

    
def main(args=None):
    rclpy.init(args=args)
    tx = bp_tx()
    rclpy.spin(tx)

    tx.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()