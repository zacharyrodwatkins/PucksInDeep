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

        self.avgx = 0
        self.avgy = 0

        self.vx = Queue() 
        self.vy = Queue()
        self.not_pub = True

        super().__init__('intercept')
        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        
        # self.puck_status_publisher = self.create_publisher(PuckStatus, 'PUCK', 10)


    def compute_dir(self):
        if(self.not_pub and self.puck_vy < -150.0):
            self.vy.put(self.puck_vy)
            self.vx.put(self.puck_vx)
            if (self.vx.qsize()>=1):
                
                l = list(self.vx.queue)
                self.avgx = sum(l)/len(l)
                
                l = list(self.vy.queue)
                self.avgy = sum(l)/len(l)
                self.not_pub = False
                print('zoom')
                print(self.avgy)
                print(self.avgx)
                self.publish_path()          
            
    def publish_path(self):
        self.mallet_t = (self.crossing_line-self.puck_y)/self.avgy
        self.mallet_x = self.puck_x+self.avgx*self.mallet_t

        msg = NextPath()
        msg.x = self.mallet_x
        msg.y = self.mallet_y
        msg.vx = 0.0
        msg.vy = 0.0
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = self.mallet_t
        self.get_logger().info("intercept")
        self.path_publisher.publish(msg)
        self.get_logger().info("published")

    def puck_callback(self, msg):
        # print('callback')
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