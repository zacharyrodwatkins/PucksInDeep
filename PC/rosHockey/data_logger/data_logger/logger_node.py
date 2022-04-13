from importlib.resources import path
from socket import MSG_CONFIRM
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus
from hockey_msgs.msg import NextPath
from hockey_msgs.msg import PuckStatus
import datetime
import os
import time

class logger_node(Node):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.m1 = 0
        self.m2 = 0
        

        os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/../data")  # So you can run from any directory
        self.file_name = str(datetime.datetime.now()) + ".json"
        self.log_file = open(self.file_name, "a")

        super().__init__('logger_node')
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
        self.path_subsciption = self.create_subscription(
            NextPath,
            'PATH',
            self.path_callback,
            10)
        self.subscription = self.create_subscription(
            PuckStatus,
            'PUCK',
            self.puck_callback,
            10)
        
        self.start_time = time.time()

    def path_callback(self, msg):
        logger_time = time.time() - self.start_time
        msg_s = '{{"PATH" : {{"x" : {}, "y" : {}, "vx" : {}, "vy" : {}, "ax" : {}, "ay" : {}, "t" : {}, "logger_time" : {}}}}}\n'\
            .format(msg.x, msg.y, msg.vx, msg.vy,msg.ax, msg.ay, msg.t, logger_time)
        self.log_file.write(msg_s)

    def puck_callback(self, msg):
        logger_time = time.time() - self.start_time
        msg_s = '{{"PUCK" : {{"x" : {}, "y" : {}, "vx" : {}, "vy" : {}, "logger_time" : {}}}}}\n'\
            .format(msg.x, msg.y, msg.x_vel, msg.y_vel, logger_time)
        self.log_file.write(msg_s)

    def mallet_callback(self, msg):
        logger_time = time.time() - self.start_time
        msg_s = '{{"MALLET" : {{"x" : {}, "y" : {}, "vx" : {}, "vy" : {}, "time_on_path" : {}, "logger_time" : {}}}}}\n'\
            .format(msg.x, msg.y, msg.vx, msg.vy, msg.time_on_path, logger_time)

        self.log_file.write(msg_s)

    def motor_callback(self,msg):
        logger_time = time.time() - self.start_time
        msg_s = '{{"MOTOR" : {{"m1" : {}, "m2" : {}, "time_on_path" : {}, "logger_time" : {}}}}}\n'\
            .format(msg.m1effort, msg.m2effort, msg.time_on_path, logger_time)
        self.log_file.write(msg_s)
                
def main(args=None):
    rclpy.init(args=args)
    logger = logger_node()
    rclpy.spin(logger)

    # Close file when node is shut down
    print("Closing log file and shutting down logger node")
    logger.log_file.close()
    logger.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
