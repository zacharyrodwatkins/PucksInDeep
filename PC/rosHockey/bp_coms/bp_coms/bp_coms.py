
import serial
from serial.serialutil import SerialException
import time
import struct
import numpy as np
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import NextPath, MotorStatus, MalletPos
TIMER_PERIOD = 1/1000
NUM_FLOATS = 7
NUM_BYTES = 4*NUM_FLOATS


class bp_coms(Node):

    def __init__(self):
        super().__init__('bp_coms')
        self.nextpath_subscription = self.create_subscription(NextPath, 'PATH', self.send_next_path, 100)
        self.ser = None

        self.mallet_publisher = self.create_publisher(MalletPos, 'MALLET', 10)
        self.motor_publisher = self.create_publisher(MotorStatus, 'MOTOR', 10)
        self.time = self.create_timer(TIMER_PERIOD, self.get_bp_data)


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
        # test_list = msg_x + 
        print (msg_x, msg_y)

        # send = [0.0,0.0,0.0,1.0,1.0,0.0,0.0,0.0,1.0,1.0]
        print(self.ser.write(struct.pack('ffffffffff', *msg_x, *msg_y)))

                    
    def get_bp_data(self):
        if (self.ser.in_waiting >= NUM_BYTES):
            mallet_status = self.ser.read(NUM_BYTES)
            floats = struct.unpack('fffffff', mallet_status)
            x,y,vx,vy,m1,m2,t = floats
            motor_msg = MotorStatus()
            mallet_msg = MalletPos()
            motor_msg.m1effort = m1
            motor_msg.m2effort = m2
            motor_msg.time_on_path = t
            mallet_msg.x = x 
            mallet_msg.y = y 
            mallet_msg.vx = vx
            mallet_msg.vy = vy
            mallet_msg.time_on_path =  t
            self.mallet_publisher.publish(mallet_msg)
            self.motor_publisher.publish(motor_msg)


def main(args=None):
    rclpy.init(args=args)
    coms = bp_coms()
    rclpy.spin(coms)

    coms.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
