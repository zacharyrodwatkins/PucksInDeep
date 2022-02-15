import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath
TIMER_PERIOD = 1/10


class HLC(Node):
  
    def __init__(self):
        self.puck_x = 0.0
        self.puck_y = 0.0
        self.puck_vx = 0.0
        self.puck_vy = 0.0

        self.crossing_line = 20.0

        self.mallet_x = 0.0
        self.mallet_y = self.crossing_line
        self.mallet_t = 0.0

        super().__init__('HLC')
        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)

    def update_path(self):
        msg = NextPath()
        msg.x = float(self.mallet_x)
        msg.y = float(self.mallet_y)
        msg.vx = 0.0
        msg.vy = 0.0
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = 0.2
        self.path_publisher.publish(msg)

    def compute_crossing_point(self):
        # print(self.puck_vy)
        # if (self.puck_vy < -0.1):
        #     self.mallet_t = (self.crossing_line-self.puck_y)/self.puck_vy
        #     self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t
        #     if (self.mallet_x< 10):
        #         self.mallet_x = 10
        #     if (self.mallet_x> 50):
        #         self.mallet_x = 50

        # else:
        #     self.mallet_x = self.puck_x
        #     self.mallet_t = 1.0
        #     if (self.mallet_x< 10):
        #         self.mallet_x = 10
        #     if (self.mallet_x> 50):
        #         self.mallet_x = 50
        self.mallet_x = self.puck_x


    def puck_callback(self, msg):
        self.puck_x = msg.x
        self.puck_y = msg.y
        self.puck_vx = msg.x_vel
        self.puck_vy = msg.y_vel

        self.compute_crossing_point()
        self.update_path()

def main(args=None):
    rclpy.init(args=args)
    hlc = HLC()
    rclpy.spin(hlc)

    hlc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()