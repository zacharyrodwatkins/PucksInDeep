import rclpy
from rclpy.node import Node
# import pandas as pd
import time
from hockey_msgs.msg import PuckStatus
(time.tim() - start)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('vel_test')
        self.start = time.time()
        self.subscription = self.create_subscription(
            PuckStatus,
            'PuckStatus',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.delta_pos = [0.0,0.0]
        # self.data = pd.dataframe()
        # self.data.columns = ["x vel", "y vel"]

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%f: %f"' % (msg.x_vel, msg.y_vel))
        # self.data = self.data.append({'x vel': msg.x_vel, 'y vel': msg.y_vel}, ignore_index=True)
        delta_t = (time.time() - self.start)
        self.start = time.time()
        self.delta_pos = [self.delta_pos[0] + msg.x_vel*delta_t, self.delta_pos[1] + msg.y_vel*delta_t]
        print("delta pos: {}".format(self.delta_pos))



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()