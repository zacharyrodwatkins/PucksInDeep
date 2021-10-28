import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from encoders.py import Encoder


class MotorPosition:
    
    def __init__(self):
        self.angle = 0
        self.rot_count = 0

class PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_publisher')
        self.encoders = [Encoder(0), Encoder(1)]
        self.motor_pos = [MotorPosition(), MotorPosition()]
        self.pulley_diam = 2.78 * 25.4  # inches to mm

        self.publisher_ = self.create_publisher(MalletPos, 'topic', 10)
        publisher_period = 0.01  # seconds
        self.pub_timer = self.create_timer(publisher_period, self.publish_callback)
        self.i = 0

        self.rot_count_threshold = 350
        self.pos_update_period = 0.0001
        self.pos_timer = self.create_timer(self.pos_update_period, self.update_motor_pos)

    def publish_callback(self):
        msg = MalletPos()
        msg.x = self.get_x()
        msg.y = self.get_y()
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg)
        self.i += 1
        
    def get_x(self):
        translations = self.get_translations()
        return -(translations[0] + translations[1])/2
    
    def get_y(self):
        translations = self.get_translations()
        return (translations[0] - translations[1])/2

    def get_translations(self):
        translations = []
        rot_to_trans = 0.0174533 * self.pulley_diam/2  # degrees to radians then multipy by radius
        for i in range(2):
            translations.append(rot_to_trans*(360*self.motor_pos[i].rot_count + self.motor_pos[i].angle))
        return translations

    def update_motor_pos(self):
        new_pos = [self.encoders[0].get_angle(), self.encoders[1].get_angle()]
        for i in range(2):
            if (self.motor_pos[i].angle - new_pos[i]) > self.rot_count_threshold:
                self.motor_pos[i].rot_count -= 1
            if (new_pos[i] - self.motor_pos[i]) > self.rot_count_threshold:
                self.motor_pos[i] += 1
            self.motor_pos.angle = new_pos


def main(args=None):
    rclpy.init(args=args)

    position_publisher = PositionPublisher()

    rclpy.spin(position_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    position_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()