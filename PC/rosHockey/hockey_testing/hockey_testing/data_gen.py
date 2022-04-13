from matplotlib import rc
from numpy import linspace
import rclpy
from rclpy.node import Node
import sys
from hockey_msgs.msg import NextPath, MalletPos
from std_msgs.msg import String
import time
from data_logger import solve_for_coefs, model_plotter
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# x_coefs = solve_for_coefs.get_coeffs((0,0,0),(30,100,0),0.1)
# y_coefs = solve_for_coefs.get_coeffs((0,0,0),(10,0,0),0.1)


# Vs = model_plotter.get_model_function(x_coefs,y_coefs)
# t = linspace(0,0.1)
# plt.plot(t, np.polyval(x_coefs,t))
# plt.plot(t, np.polyval(y_coefs,t))
# plt.plot(t, Vs(t)[0])
# plt.plot(t, Vs(t)[1])
# plt.show()

class DataGenNode(Node):

    def __init__(self):
        super().__init__("data_gen")
        self.path_publisher = self.create_publisher(NextPath, "PATH", 1)

        self.mallet_subscription = self.create_subscription(
            MalletPos,
            'MALLET',
            self.mallet_callback,
            1)
        

        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.time_on_path = None

        self.fin_x_bounds = [20,60]
        self.fin_y_bounds = [20,80]

        self.abs_x_bounds = [0,85]
        self.abs_y_bounds = [0,104]
        
        self.final_vel_bounds = [-500, 500]
        self.t_bound = [0.05,2]
        self.V_bounds = [-20,20]

    def mallet_callback(self,msg):
        self.x = msg.x
        self.y = msg.y
        self.vx = msg.vx
        self.vy = msg.vy
        self.time_on_path = msg.time_on_path
    
    def gen_path(self):
        while True:
            fin_x = np.random.uniform(low=self.fin_x_bounds[0],high=self.fin_x_bounds[1])
            fin_y = np.random.uniform(low=self.fin_y_bounds[0],high=self.fin_y_bounds[1])
            fin_vx,fin_vy = tuple(np.random.uniform(low=self.final_vel_bounds[0],high=self.final_vel_bounds[1], size=2))
            Dt = np.random.uniform(low=self.t_bound[0], high=self.t_bound[1])
            x_coefs  = solve_for_coefs.get_coeffs((self.x, 0, 0), (fin_x, fin_vx,0),Dt) 
            y_coefs  = solve_for_coefs.get_coeffs((self.y,0,0), (fin_y, fin_vy,0),Dt)
            t = np.linspace(0,Dt)
            x_pred = np.polyval(x_coefs, t)
            y_pred = np.polyval(y_coefs,t)

            voltage_func = model_plotter.get_model_function(x_coefs,y_coefs)
            voltage = voltage_func(t)


            if not (((x_pred >= self.abs_x_bounds[0]).all()) and (x_pred<=self.abs_x_bounds[1]).all()\
                and (y_pred >= self.abs_y_bounds[0]).all() and (y_pred<=self.abs_y_bounds[1]).all()):
                continue


            if not ((np.array(voltage)>self.V_bounds[0]).all() and (np.array(voltage)<self.V_bounds[1]).all()):
                continue

            return (fin_x, fin_y, fin_vx, fin_vy, Dt)


    def send_rand_path(self):
        msg = NextPath()
        msg.x, msg.y, msg.vx, msg.vy, msg.t = self.gen_path()
        msg.ax = 0.0 
        msg.ay = 0.0
        self.path_publisher.publish(msg)
        return msg.t

if __name__ == "__main__":
    rclpy.init()
    n = DataGenNode()
    while(True):
        rclpy.spin_once(n)
        dt = n.send_rand_path()
        time.sleep(dt+1.5)
        print("here")
        
