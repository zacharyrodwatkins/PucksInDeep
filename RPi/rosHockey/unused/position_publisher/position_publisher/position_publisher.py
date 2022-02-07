import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
try:
    from position_publisher.encoder import Encoder
except ModuleNotFoundError:
    from encoder import Encoder

class MotorPosition:
    
    def __init__(self):
        self.angle = 0
        self.rot_count = 0
        self.vel = 0
        self.thresh_time = time.time()

class PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_publisher')
        self.encoders = [Encoder(0), Encoder(1)]
        self.motor_pos = [MotorPosition(), MotorPosition()]
        self.pulley_diam = 2.78 * 25.4  # inches to mm

        self.publisher_ = self.create_publisher(MalletPos, 'MalletPosition', 10)
        publisher_period = 0.01  # seconds
        self.pub_timer = self.create_timer(publisher_period, self.publish_callback)
        self.i = 0

        self.rot_count_threshold = 350
        self.pos_update_period = 1/1e8
        self.pos_timer = self.create_timer(self.pos_update_period, self.update_motor_pos)

    def publish_callback(self):
        msg = MalletPos()
        msg.x = self.get_x()
        msg.y = self.get_y()
        self.publisher_.publish(msg)
        print('a0: %d . %f     a1: %d . %f' % (self.motor_pos[0].rot_count, self.motor_pos[0].angle, self.motor_pos[1].rot_count, self.motor_pos[1].angle))
        # print('"%s"' % msg)
        # print('vel motor 1 %.3f vel motor 2 %.3f' % (self.motor_pos[0].vel, self.motor_pos[1].vel))
        self.i += 1
        
    def get_x(self):
        translations = self.get_translations()
        return -(translations[0] + translations[1])/2
    
    def get_y(self):
        translations = self.get_translations()
        return -(translations[0] - translations[1])/2

    def get_translations(self):
        translations = []
        rot_to_trans = 0.0174533 * self.pulley_diam/2  # degrees to radians then multipy by radius
        for i in range(2):
            translations.append(rot_to_trans*(360*self.motor_pos[i].rot_count + self.motor_pos[i].angle))
        # print(translations)
        return translations

    def update_motor_pos(self):
        new_pos = [self.encoders[0].get_angle(), self.encoders[1].get_angle()]
        if None in new_pos:
            return
        for i in range(2):
            if (self.motor_pos[i].angle - new_pos[i]) > self.rot_count_threshold:
               
                self.motor_pos[i].rot_count += 1
                time_now = time.time()
                time_elapsed = (time_now - self.motor_pos[i].thresh_time)
                self.motor_pos[i].vel = 1/time_elapsed #angularvel in rotations/second
                self.motor_pos[i].thresh_time = time_now
            if (new_pos[i] - self.motor_pos[i].angle) > self.rot_count_threshold:
                self.motor_pos[i].rot_count -= 1
                time_now = time.time()
                time_elapsed = (time_now - self.motor_pos[i].thresh_time)
                self.motor_pos[i].vel = 1/time_elapsed #angularvel in rotations/second
                self.motor_pos[i].thresh_time = time_now
            self.motor_pos[i].angle = new_pos[i]



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