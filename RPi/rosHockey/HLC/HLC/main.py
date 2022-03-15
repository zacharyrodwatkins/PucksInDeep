import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath
from statistics import mean
TIMER_PERIOD = 1/10


class HLC(Node):
  
    def __init__(self):
        self.time =time.time()
        
        # Puck status variables
        self.puck_x = 0.0
        self.puck_y = 0.0
        self.puck_vx = 0.0
        self.puck_vy = 0.0

        #  Table geometry
        self.midline = 80  # cm
        self.goal_range = (26.5, 26.5+25.4)

        #  Decision variables
        self.last_path_time = time.time()
        self.crossing_line = 0.0  # Default defensive intercept line is goal line
        self.threshold_time = 0.05  # 50 ms
        self.too_fast = self.midline/0.5  # Will hit back wall in under 0.5 sec
        self.v_shot = 80.0  # hit puck while going 40 cm/s
        self.t_shot = 0.5  # hit puck for shot 0.3 sec after crossing midline

        # Path variables (final acceleration is unused at the moment, maybe good if you know the following path)
        self.mallet_x = 0.0
        self.mallet_y = 0.0
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
        self.mallet_t = 0.0

        super().__init__('HLC')
        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)

    def update_path(self):
        self.time = time.time()
        msg = NextPath()
        msg.x = float(self.mallet_x)
        msg.y = float(self.mallet_y)
        msg.vx = self.mallet_vx
        msg.vy = self.mallet_vy
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = self.mallet_t
        self.get_logger().info("intercept")
        self.path_publisher.publish(msg)
        self.get_logger().info("published`")

    def load_defensive_path(self):
        self.mallet_t = (self.crossing_line-self.puck_y)/self.puck_vy
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t
        self.mallet_y = self.crossing_line
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
    
    def load_offensive_path(self):
        self.mallet_t = self.t_shot
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t
        self.mallet_y = self.puck_y+self.puck_vy*self.mallet_t
        delta_x = mean(self.goal_range)-self.mallet_x
        delta_y = self.midline*2 - self.mallet_y
        self.mallet_vx = self.v_shot * delta_x/(delta_x**2 + delta_y**2)**(1/2)
        self.mallet_vy = self.v_shot * delta_y/(delta_x**2 + delta_y**2)**(1/2)

    def load_center(self):
        self.mallet_t = 1.0
        self.mallet_x = 40.0
        self.mallet_y = 10.0
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0

    def puck_callback(self, msg):
        # Get puck status
        self.puck_x = msg.x
        self.puck_y = msg.y
        self.puck_vx = msg.x_vel
        self.puck_vy = msg.y_vel

 

        # If we havent finished our last path don't do anything
        if (time.time() - self.last_path_time) < self.mallet_t:
            return

        # If shot is coming our way
        self.last_path_time = time.time()
        if self.crossing_midline():

            # If puck is not too fast
            if (abs(self.puck_vy) < self.too_fast):
                self.load_offensive_path()
                self.update_path()
                
                print("nice and slow")
            # If puck is too fast
            else:
                # Get x and t at which puck will cross the goal line
                self.load_defensive_path()
                # If that x value is within the goal, move to block
                if self.mallet_x > self.goal_range[0] and self.mallet_x < self.goal_range[1]:
                    self.update_path()
                # Otherwise we are fine to chill
                else:
                    print("not on target ;)")   
        else:
             self.load_center()
             print("center")
             self.update_path()   

    def crossing_midline(self):
        
        if self.puck_x<0:
            # Lost puck, just go pack to center
            return False
        if self.puck_vy > 20:
            # Not moving towards, us we dont care
            return False
        if (self.puck_y + (self.puck_vy * self.threshold_time)) < self.midline:
            # Puck is on opponents end and coming at us
            return True
        print('not headed to our side')

        return False

def main(args=None):
    rclpy.init(args=args)
    hlc = HLC()
    rclpy.spin(hlc)

    hlc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()