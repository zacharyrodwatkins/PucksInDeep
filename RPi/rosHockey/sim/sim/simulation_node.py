import rclpy
from rclpy.node import Node
from hockey_msgs.msg import MalletPos
from hockey_msgs.msg import MotorStatus
from hockey_msgs.msg import NextPath
from hockey_msgs.msg import PuckStatus
import datetime
import os
import time
import numpy as np
from solve_for_coefs import get_all_functions

class sim_node(Node):

    def __init__(self):

        self.path_subsciption = self.create_subscription(
            NextPath,
            'PATH',
            self.path_callback,
            10)

        self.next_path_msg = None
        self.start_time  = time.time()
        self.new_path_time = 0
        self.prev_path_time = 0
        self.path_func = lambda t : np.zeros((3,2))


    #pass start x,v,a
    def _make_function(self, stop, t):
        start = self.path_func(t)
        # self.path_s
        

    def path_callback(self, msg):
        self.next_path_msg = msg
        self.prev_path_time = self.new_path_time
        self.new_path_time = time.time()-self.start_time
        




        