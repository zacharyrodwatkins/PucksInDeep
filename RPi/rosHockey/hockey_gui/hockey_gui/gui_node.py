import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus
from hockey_msgs.msg import NextPath

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

        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)


    def mallet_callback(self, msg):
        self.x = msg.x*10
        self.y = msg.y*10

    def motor_callback(self,msg):
        self.m1 = msg.m1effort
        self.m2 = msg.m2effort

    def send_path(self,x,y,vx,vy,ax,ay,t):
        msg = NextPath()
        msg.x = x/10
        msg.y = y/10
        msg.vx = vx/10
        msg.vy = vy/10
        msg.ax = ax/10
        msg.t = t
        self.path_publisher.publish(msg)
