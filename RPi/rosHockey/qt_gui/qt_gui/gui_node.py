import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus

class gui_node(Node):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.m1 = 0
        self.m2 = 0

        super().__init__('gui_node')
        self.mallet_subscription = self.create_subscription(
            MalletPos,
            'MALLET',
            self.mallet_callback,
            1)
        self.motor_subscription = self.create_subscription(
            MotorStatus,
            'MOTOR',
            self.motor_callback,
            1)


    def mallet_callback(self, msg):
        self.x = msg.x
        self.y = msg.y

    def motor_callback(self,msg):
        self.m1 = msg.m1effort
        self.m2 = msg.m2effort





