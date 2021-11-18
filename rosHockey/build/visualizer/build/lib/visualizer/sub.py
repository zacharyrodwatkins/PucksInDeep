import rclpy
from rclpy.node import Node

from hockey_msgs.msg import MalletPos


class EncoderSubscriber(Node):

    def __init__(self,callback):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            MalletPos,
            'MalletPosition',
            callback,
            10)
        self.subscription  # prevent unused variable warnin

    def listener_callback(self, msg):
        self.get_logger().info(str(msg))


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = EncoderSubscriber(None)

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()