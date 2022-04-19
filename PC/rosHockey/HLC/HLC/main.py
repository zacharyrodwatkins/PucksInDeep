import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath, MalletPos
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

        # Mallet Status Variables
        self.mallet_current_x = 0.0
        self.mallet_current_y = 0.0

        # Max average velocity of different path types
        self.vel_offense = 180.0
        self.vel_defense = 200.0
        self.vel_home = 40.0

        # Absolute max final velocity
        self.vel_absolute_max = 250.0

        # Gantry Dimensions, this defines the playable area
        self.gantry_dimensions_y = (10.0,87.0)
        self.gantry_dimensions_x = (0, 86.0)

        #Table and accessory dimensions
        self.midline = 80  # cm this defines our home zone
        self.goal_line = 200 #distance to opposing net
        self.mallet_radius = 5
        self.puck_radius = 3.1

        #Goal dimensions, right now set to table width as it's more interesting to 
        # block every shot for demo purposes (although strategically unnecessary)
        # Right now this is only used to determine offensive shot direction
        self.goal_range = (0, 92.7)

        # Table width, this is used to compute final position of bounce shots
        self.table_range = (0,92.7)


        #  Decision variables
        self.last_path_time = time.time()

        self.crossing_line = 10.0  # Default defensive intercept line is goal line
        self.threshold_time = 0.05  # 50 ms, how far ahead of the puck trajectory are we looking at when we decide off vs def
        
        # If incoming vel is too fast, go to defensive path
        self.too_fast =  70 #set defensive flag
        self.v_shot = 200.0  # velocity of offensive path 220 is great!
        self.t_shot = 0.4  # path time for offensive path
        self.defensive_path_factor = 1 #get to puck faster than we expect based on camera lag
        self.min_mallet_t = 0.3 #prevent defensive paths from being under this time, small path times are unstable
        

        # Path Type Flags
        self.positive_velocity = True
        self.start_defense_loop = 0.0
        self.home = False
        self.offensive_flag = False

        # Path variables (final acceleration is unused at the moment, maybe good if you know the following path)
        self.mallet_x = 0.0
        self.mallet_y = 0.0
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
        self.mallet_t = 0.0

        super().__init__('HLC')

        # Initiate ROS the Boss Rhea Nodes
        self.puck_status_subscription = self.create_subscription(PuckStatus,'PUCK',self.puck_callback,10)
        self.path_publisher = self.create_publisher(NextPath, 'PATH', 10)
        self.mallet_status_subscription = self.create_subscription(MalletPos, 'MALLET', self.mallet_callback, 10)
        self.puck_status_publisher = self.create_publisher(PuckStatus, 'PuckStatus', 10)

    def update_path(self):

        # Check path variables against preset limits (should do this with min max)
        if (self.mallet_x>self.gantry_dimensions_x[1]):
            self.mallet_x = self.gantry_dimensions_x[1]
        if (self.mallet_x<self.gantry_dimensions_x[0]):
            self.mallet_x = self.gantry_dimensions_x[0]

        if (self.mallet_y>self.gantry_dimensions_y[1]):
            self.mallet_y = self.gantry_dimensions_y[1]
        if (self.mallet_y<self.gantry_dimensions_y[0]):
            self.mallet_y = self.gantry_dimensions_y[0]

        if self.mallet_vx > self.vel_absolute_max:
            self.mallet_vx = self.vel_absolute_max
        if self.mallet_vx < -1*self.vel_absolute_max:
            self.mallet_vx = -1*self.vel_absolute_max
        
        if self.mallet_vy > self.vel_absolute_max:
            self.mallet_vy = self.vel_absolute_max
        if self.mallet_vy < -1*self.vel_absolute_max:
            self.mallet_vy = -1*self.vel_absolute_max

        self.time = time.time()
        msg = NextPath()
        msg.x = float(self.mallet_x)
        msg.y = float(self.mallet_y)

        msg.vx = float(self.mallet_vx)
        msg.vy = float(self.mallet_vy)
        msg.ax = 0.0
        msg.ay = 0.0
        msg.t = self.mallet_t
        # self.get_logger().info("intercept")
        self.path_publisher.publish(msg)
        # self.get_logger().info("published`")


    # Get in front of puck ASAP
    def load_defensive_path(self):
        
        # Figure out when and where the puck will cross crossing line
        self.mallet_t = (self.crossing_line-self.puck_y)/self.puck_vy
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t


        # Bounce mechanics
        if (self.mallet_x > self.table_range[1]):
            self.mallet_x = self.table_range[1]
        
        if (self.mallet_x < self.table_range[0]):
            self.mallet_x = self.table_range[0]

        self.mallet_y = self.crossing_line-self.mallet_radius
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0

        # camera lag factor, fuckn nitro
        self.mallet_t = self.mallet_t/self.defensive_path_factor

        distance = self.compute_distance()
        self.going_too_fast(self.vel_defense, distance)

    
    # Shoot puck towards opposing goal
    def load_offensive_path(self):
        self.mallet_t = self.t_shot
        self.mallet_x = self.puck_x+self.puck_vx*self.mallet_t
        self.mallet_y = self.puck_y+self.puck_vy*self.mallet_t

        delta_x = mean(self.goal_range)-self.mallet_x
        delta_y = self.goal_line - self.mallet_y-self.mallet_radius

        direction_x = delta_x/(delta_x**2 + delta_y**2)**(1/2)
        direction_y = delta_y/(delta_x**2 + delta_y**2)**(1/2)

        # Hit the mallet at correct angle
        self.mallet_x = self.mallet_x-direction_x*(self.mallet_radius+self.puck_radius)
        self.mallet_y = self.mallet_y-direction_y*(self.mallet_radius+self.puck_radius)

        self.mallet_vx = self.v_shot * direction_x
        self.mallet_vy = self.v_shot * direction_y 

        distance = self.compute_distance()
        self.going_too_fast(self.vel_offense, distance)


    # play along the back of the net, default posiction
    def load_center(self):
        self.mallet_t = 0.7
        self.mallet_x = (self.table_range[1]-self.table_range[0])/2.0
        self.mallet_y = self.crossing_line
        self.mallet_vx = 0.0
        self.mallet_vy = 0.0
        self.home = True

        distance = self.compute_distance()
        self.going_too_fast(self.vel_home, distance)
        print("home")

    def puck_callback(self, msg):
        # Get puck status
        self.puck_x = msg.x
        self.puck_y = msg.y
        self.puck_vx = msg.x_vel
        self.puck_vy = msg.y_vel

    # Compute distance between initial and desired position
    def compute_distance(self):
        del_x = self.mallet_x-self.mallet_current_x
        del_y = self.mallet_y-self.mallet_current_y

        return ((del_x**2+del_y**2)**(1/2))

    # If the average velocity exceeds threshhold, loosen time requirement
    def going_too_fast(self, vel, distance):
        if (distance/self.mallet_t>vel):
            self.mallet_t = distance/vel
            print("path time too short")


    def mallet_callback(self, msg):
        self.mallet_current_x = msg.x
        self.mallet_current_y = msg.y


        # If we havent finished our last path don't do anything, there's a time lag here
        if ((time.time() - self.last_path_time) < self.mallet_t):

            # After an offensive path go back to home
            if(self.offensive_flag):
                return

            # Don't interrupt a homing path
            if (not self.home):
                return

            # After a defensive path go pack to home
            if (not self.positive_velocity and time.time()-self.start_defense_loop< 0.12):
                return

        
        # Return to home after offensive path
        if (self.offensive_flag and not self.home):
            self.load_center()
            self.update_path()
            print("goin home")
            self.home = True

        # Check to see if puck is in our zone, do nothing otherwise
        elif self.crossing_midline():
            self.last_path_time = time.time()
            self.home = False
            self.offensive_flag = False

            # If puck is going slow enough, take a shot
            if (abs(self.puck_vy) < self.too_fast):
                self.load_offensive_path()
                self.update_path()
                self.offensive_flag = True
                print("offense!")

            # If puck is too fast
            else:
                # Get x and t at which puck will cross the goal line
                print("defense!")
                        # bounce mechanics
                if (self.mallet_x < self.table_range[0]):
                    self.mallet_x = 2*self.table_range[0]-self.mallet_x
                elif (self.mallet_x > self.table_range[1]):
                    self.mallet_x = 2*self.table_range[1]-self.mallet_x
                self.load_defensive_path()

                self.update_path()
                self.positive_velocity = False
                self.start_defense_loop = time.time()

        else:
            if not self.home:
                self.load_center()
                print("center")
                self.update_path()


    # Figure out whether to take a shot
    # A few of these conditions are just for safety
    def crossing_midline(self):

        if self.puck_vy > 0:
            self.positive_velocity = True
        
        # puck is too close to our goal lines
        # Don't want figures to get hit so do nothing
        if self.puck_y<20:
            # Lost puck, just go pack to center
            return False

        if self.puck_vy > 100:
            # print("movin back")
            # Not moving towards, us we dont care
            return False
        
        # Only take a defensive/offensive shot if puck is in our zone
        if (self.puck_y) < self.midline:
            print("crossing")
            # Puck is on opponents end and coming at us
            return True
        # print('not headed to our side')

        return False

def main(args=None):
    rclpy.init(args=args)
    hlc = HLC()
    rclpy.spin(hlc)

    hlc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()