from os import read
import serial
import numpy as np
import matplotlib.pyplot as plt
import rclpy
from rclpy.node import Node

from hockey_msgs.msg import MotorStatus, NextPath


class MotorSubscriber(Node):

    def __init__(self):
        super().__init__('motor_subscriber')
        self.subscription = self.create_subscription(
            MotorStatus,
            'MOTOR',
            self.listener_callback,
            10)
        self.publisher_ = self.create_publisher(NextPath, 'PATH', 10)
        self.V1 = []
        self.V2 = []
        self.t = []
        self.path_time = 0.5
        self.path_steps = 500
        self.subscription  # prevent unused variable warning

        
    def publish(self):
        msg = NextPath()
        msg.x = 69.0
        msg.y = 69.0
        msg.vx = 69.0
        msg.vy = 69.0
        msg.ax = 69.0
        msg.ay = 69.0
        msg.t = 69.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.x)
        
    def listener_callback(self, msg):
        path_time = 0.5
        path_steps = 500
        
        self.V1.append(msg.m1effort)
        self.V2.append(msg.m2effort)
        self.t.append(msg.time_on_path)
        print(len(self.V1))
        if (len(self.V1) == path_steps):
            print(self.V1)
            print(self.V2)

            for i in range(len(self.t)):
                if self.t[i] == 1:
                    self.t = self.t[-1*i:] + self.t[:-1*i]
                    self.V1 = self.V1[-1*i:] + self.V1[:-1*i]
                    self.V2 = self.V2[-1*i:] + self.V2[:-1*i]

            # t = np.linspace(0, self.path_time, self.path_steps)
            plt.scatter(self.t, self.V1)
            plt.scatter(self.t, self.V2)
            plt.legend(["m1effort", "m2effort"])
            plt.show()
            if not (input("send? (Y/n)") == "n"):
                self.publish()
            else:
                print("should save V1/V2 here")
            self.V1 = []
            self.V2 = []
            self.t = []

        self.get_logger().info('M1:%s    M2:%s' % (msg.m1effort, msg.m2effort))


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MotorSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()


# ser = serial.Serial('/dev/ttyUSB0',460800, timeout=1)

# path_time = 0.5
# path_steps = 500
# V1 = []
# V2 = []
# for i in range(path_steps*2):
#     if i < 500:
#         V1.append(ser.readline().rstrip()[2:-1])
#     else:
#         V2.append(ser.readline().rstrip()[2:-1])

# print(V1)
# print(V2)

# t = np.linspace(0, path_time, path_steps)
# plt.plot(t, V1)
# plt.plot(t, V2)
# plt.yticks(list(np.linspace(0,127,12)))
# plt.legend(["V1", "V2"])
# plt.show()