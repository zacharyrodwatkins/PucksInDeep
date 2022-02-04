from os import read
import serial
from serial.serialutil import SerialException
import time
import struct
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus
NUM_FLOATS = 7
NUM_BYTES = 4*NUM_FLOATS
TIMER_PERIOD = 5/1000


class bp_rx(Node):

    def __init__(self):
        super().__init__('bp_rx')
        self.mallet_publisher = self.create_publisher(MalletPos, 'MALLET', 10)
        self.motor_publisher = self.create_publisher(MalletPos, 'MOTOR', 10)
        self.time = self.create_timer(TIMER_PERIOD, self.get_bp_data)
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

            
    def get_bp_data(self):
        if (self.ser.in_waiting == NUM_BYTES):
            mallet_status = self.ser.read(NUM_FLOATS)
            floats = struct.unpack('fffffff', mallet_status)
            x,y,vx,vy,m1,m2,t = floats
            motor_msg = MotorStatus()
            mallet_msg = MalletPos()
            motor_msg.M1_effort = m1
            motor_msg.M2_effort = m2
            motor_msg.time_on_path = t
            mallet_msg.x = x 
            mallet_msg.y = y 
            mallet_msg.x_vel = x_vel
            mallet_msg.y_vel = y_vel
            mallet_msg.time_on_path =  time_on_path
            self.mallet_publisher.publish(mallet_msg)
            self.motor_publisher.publish(motor_msg)
    

    
def main(args=None):
    rclpy.init(args=args)
    rx = bp_rx()
    rclpy.spin(Mrx)

    rx.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()