import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import NextPath
import numpy as np

class ID_tool(Node):

    def __init__(self):
        super().__init__('puck_tracker')

        # Puck status publisher
        self.publisher = self.create_publisher(NextPath, 'PATH', 10)
        self.path_start = time.time()
        self.path_time = 0

        while (1):
            self.publish_callback()
    
    def publish_callback(self):
        if (time.time() > self.path_start+self.path_time):
            msg = NextPath()
            while (1):
                msg.x = float(input("\nPath Type?\nStep  1\nDouble Step  2\nRamp  3\nTriangle  4\n"))
                if (msg.x in (1,2,3,4,5)):
                    break
                print("\n-------Invalid input--------\n\n")
            while (1):
                msg.y = float(input("\nDirection?\ny  0\nx  1\n"))
                if (msg.y in (0,1)):
                    break
                print("\n-------Invalid input--------\n\n")
            while(1):
                msg.vx = float(input("\nTime?\n"))
                self.path_time = msg.vx
                if (msg.vx > 0):
                    break
                print("\n-------Invalid input--------\n\n")
            while (1):
                msg.vy = float(input("\nMax Voltage?"))
                if (msg.vy > 0):
                    break
                print("\n-------Invalid input--------\n\n")
            self.publisher.publish(msg)
            self.path_start = time.time()
            print("\n\nPublishing path...\n")


def main(args=None):
    rclpy.init(args=args)

    tool = ID_tool()

    rclpy.spin(tool)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)\
    tool.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
