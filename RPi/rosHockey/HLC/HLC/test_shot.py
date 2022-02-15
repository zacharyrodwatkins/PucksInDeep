from asyncio.unix_events import DefaultEventLoopPolicy
from time import sleep
import rclpy
from rclpy.node import Node
from random import randrange
from hockey_msgs.msg import PuckStatus, NextPath
TIMER_PERIOD = 1/1000
PATH_RESET_PERIOD = 5


class Fake_Shot(Node):
  
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.vx = 0.0
        self.vy = 0.0

        self.counter = 0


        super().__init__('fake_shot')
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)
        self.time = self.create_timer(TIMER_PERIOD, self.publish_puck_status)
        self.reset = self.create_timer(PATH_RESET_PERIOD, self.reset_puck)

    def publish_puck_status(self):
        if self.counter%20 == 0:
            msg = PuckStatus()
            msg.x = self.x
            msg.y = self.y
            msg.x_vel = self.vx
            msg.y_vel= self.vy
            self.puck_status_publisher.publish(msg)
        self.update_status()
        self.counter = self.counter + 1

    def reset_puck(self):
        self.x = randrange(0, 75)*1.0
        self.y = randrange(45, 55)*1.0

        self.vx = randrange(-15,15)*1.0
        self.vy = -1*randrange(1, 25)*1.0

        self.update_status()

    def update_status(self):
        step = .01
        self.y = self.y+self.vy*step
        self.x = self.x+self.vx*step
        if self.y<20:
            self.y = 20.0
            self.vy = 0.0
            self.vx = 0.0
        
        if self.x>75:
            self.vx = 0.0
            self.x = 75.0

        if self.x<0:
            self.vx = 0.0
            self.x = 0.0
        
        sleep(step)
            


def main(args=None):
    rclpy.init(args=args)
    fake_shot = Fake_Shot()
    rclpy.spin(fake_shot)

    fake_shot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()