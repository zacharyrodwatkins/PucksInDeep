import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath
import math
from queue import Queue
import numpy as np


class Intercept(Node):
  
    def __init__(self):
        self.puck_x = 0.0
        self.puck_y = 0.0
        self.puck_vx = 0.0
        self.puck_vy = 0.0

        self.crossing_line = 20.0

        self.mallet_x = 0.0
        self.mallet_y = self.crossing_line
        self.mallet_t = 0.0

        self.q = Queue() 
        self.not_pub = True

        super().__init__('intercept')
        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)


    def compute_dir(self):
        if(self.not_pub and self.puck_vy < -10.0):
            dir = math.atan(self.puck_vx/self.puck_vy)+ math.pi/2
            self.q.put(dir)
            if (self.q.qsize()>5):
                l = list(self.q.queue)
                std = np.std(l)
                if (std<0.1):
                    self.not_pub = False
                    self.publish_path()
                self.q.get()
            
            
    def publish_path(self):
        self.mallet_t = (self.crossing_line-self.puck_y)/self.puck_vy
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t

        msg = NextPath()
        msg.x = self.mallet_x
        msg.y = self.mallet_y
        msg.vx = 0.0
        msg.vy = 0.0
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = self.mallet_t
        self.path_publisher.publish(msg)

    def puck_callback(self, msg):
        self.puck_x = msg.x
        self.puck_y = msg.y
        self.puck_vx = msg.x_vel
        self.puck_vy = msg.y_vel

        self.compute_dir()



def main(args=None):
    rclpy.init(args=args)
    intercept = Intercept()
    rclpy.spin(intercept)

    intercept.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()