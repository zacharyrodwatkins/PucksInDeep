import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus
import datetime
import os


class logger_node(Node):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.v_x = 0
        self.v_y = 0
        self.m1 = 0
        self.m2 = 0

        os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/../data")  # So you can run from any directory
        self.file_name = str(datetime.datetime.now()) + ".csv"
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


    def mallet_callback(self, msg):
        self.x = msg.x*10
        self.y = msg.y*10
        self.v_x = msg.v_x*10
        self.v_y = msg.v_y*10

        # BP_rx node writes mallet first, then motor status, but I'm not sure how ROS's 
        # Synching works, so some manual synching might be necessary
        # Could be done with dataframe
        # If log file is out of order, we can make that change
        self.log_file.write("{},{},{},{},".format(self.x, self.y, self.v_x, self.v_y))

    def motor_callback(self,msg):
        self.m1 = msg.m1effort
        self.m2 = msg.m2effort

        self.log_file.write("{},{},{}\n".format(self.m1, self.m2, msg.time_on_path))
                
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