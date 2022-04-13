import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath
from statistics import mean

class Path:
    def __init__(self):
        self.interruptable = False
        # Path variables (final acceleration is unused at the moment, maybe good if you know the following path)
        self.mallet_x = 0.0
        self.mallet_y = 0.0
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
        self.mallet_t = 0.0



class OffensivePath(Path):

    def __init__(self):
        super().__init__()
        self.interruptable = False

        self.mallet_t = self.t_shot
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t
        self.mallet_y = self.puck_y+self.puck_vy*self.mallet_t

        delta_x = mean(self.goal_range)-self.mallet_x
        delta_y = self.goal_line - self.mallet_y-self.mallet_radius

        direction_x = delta_x/(delta_x**2 + delta_y**2)**(1/2)
        direction_y = delta_y/(delta_x**2 + delta_y**2)**(1/2)

        # print(self.mallet_y)
        # print(direction_x)
        # print(direction_y)

        self.mallet_x = self.mallet_x-direction_x*(self.mallet_radius+self.puck_radius)
        self.mallet_y = self.mallet_y-direction_y*(self.mallet_radius+self.puck_radius)
        self.mallet_vx = self.v_shot * direction_x
        print("offense")

class DefensivePath(Path):
    def __init__(self):
        super().__init__()
        self.interruptable = False
            
        self.mallet_t = (self.crossing_line-self.puck_y)/self.puck_vy
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t


        # bounce mechanics
        if (self.mallet_x < self.table_range[0]):
            self.mallet_x = 2*self.table_range[0]-self.mallet_x
        elif (self.mallet_x > self.table_range[1]):
            self.mallet_x = 2*self.table_range[1]-self.mallet_x



        self.mallet_y = self.crossing_line-self.mallet_radius
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0

        # camera lag factor, fuckn nitro
        self.mallet_t = self.mallet_t/self.defensive_path_factor

        # unstable paths
        if self.mallet_t < self.min_mallet_t:
            self.mallet_t = self.min_mallet_t
        print("defense")

class HomingPath(Path):
    def __init__(self):
        super().__init__()
        self.interruptable = True

        self.mallet_t = 0.5
        self.mallet_x = (self.table_range[1]-self.table_range[0])/2.0
        self.mallet_y = 15.0
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
        self.home = True


class HLC(Node):
  
    def __init__(self):

        self.time =time.time()
        
        # Puck status variables
        self.puck_x = 0.0
        self.puck_y = 0.0
        self.puck_vx = 0.0
        self.puck_vy = 0.0

         #  Table geometry
        self.midline = 90  # cm
        self.goal_line = 123
        self.mallet_radius = 5
        self.puck_radius = 3.1
         # self.goal_range = (26.5, 26.5+25.4)
        self.goal_range = (10, 70)
        self.table_range = (0,89)


        #  Decision variables
        self.last_path_time = time.time()

        self.crossing_line = 20.0  # Default defensive intercept line is goal line
        self.threshold_time = 0.05  # 50 ms, how far ahead of the puck trajectory are we looking at when we decide off vs def
        self.too_fast =  150 #set defensive flag
        self.v_shot = 220.0  # velocity of offensive path
        self.t_shot = 0.35  # path time for offensive path
        self.defensive_path_factor = 1.8 #get to puck faster than we expect based on camera lag
        self.min_mallet_t = 0.1 #prevent defensive paths from being under this time, small path times are unstable
        self.home = False
        self.offensive_flag = False

        super().__init__('HLC')

        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)

    def get_new_path(self):
        self.last_path_time = time.time()
        if self.crossing_midline():
            self.offensive_flag = False
            self.home = False
            # If puck is not too fast
            print(self.puck_vy)

            if (abs(self.puck_vy) < self.too_fast):
                return 1


            # If puck is too fast
            else:
                # Get x and t at which puck will cross the goal line
                if self.mallet_x > self.goal_range[0] and self.mallet_x < self.goal_range[1]:
                    return 2
        else:
            if not self.home:
                return 0


    def update_path(path, self):
        self.time = time.time()
        msg = NextPath()
        msg.x = float(path.mallet_x)
        msg.y = float(path.mallet_y)
        msg.vx = path.mallet_vx
        msg.vy = path.mallet_vy
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = path.mallet_t
        # self.get_logger().info("intercept")
        self.path_publisher.publish(msg)
        # self.get_logger().info("published`")

    def crossing_midline(self):
            
            # puck is too close to our goal line
            if self.puck_y<20:
                # Lost puck, just go pack to center
                return False
            if self.puck_vy > 20:
                # print("movin back")
                # Not moving towards, us we dont care
                return False
            if (self.puck_y + (self.puck_vy * self.threshold_time)) < self.midline:
                # Puck is on opponents end and coming at us
                return True
            # print('not headed to our side')

            return False

    def puck_callback(self, msg):
        # Get puck status
        self.puck_x = msg.x
        self.puck_y = msg.y
        self.puck_vx = msg.x_vel
        self.puck_vy = msg.y_vel

def main(args=None):
    rclpy.init(args=args)
    hlc = HLC()
    path = Path()

    path_library = [HomingPath,OffensivePath,DefensivePath]

    while(True):

        rclpy.spin_once(hlc)

        # If we havent finished our last path don't do anything, there's a time lag here
        if ((time.time() - hlc.last_path_time) < path.mallet_t+0.1):
            path = path_library[hlc.get_new_path()]()
            if path.interruptable:
                hlc.update_path()