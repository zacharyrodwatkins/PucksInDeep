import rclpy
from rclpy.node import Node
import time
from hockey_msgs.msg import PuckStatus
import matplotlib.pyplot as plt


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            PuckStatus,
            'PUCK',
            self.listener_callback,
            10)
        self.time_stamp = time.time()
        self.periods = []
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        period = time.time() - self.time_stamp
        self.periods.append(period)
        self.time_stamp = time.time()


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()
    try:
        rclpy.spin(minimal_subscriber)
    except:
        del minimal_subscriber.periods[0]
        del minimal_subscriber.periods[-1]
        print("avg per: {}    max dur: {}".format(sum(minimal_subscriber.periods)/len(minimal_subscriber.periods), max(minimal_subscriber.periods)))
        plt.figure(1)
        plt.subplot(211)
        plt.plot(minimal_subscriber.periods)
        plt.subplot(212)
        plt.hist(minimal_subscriber.periods, 20)
        plt.show()
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()