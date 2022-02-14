import rclpy
from rclpy.node import Node
import sys
from hockey_msgs.msg import NextPath
from std_msgs.msg import String
import time
default_test = "test_files/default.txt"


def parse_line(line):
    msg = NextPath()
    line_strings = line.split()
    print()
    args  = [float(s) for s in line_strings[:7]]
    print(args)
    if len(line_strings)>=8:
        execute_time = line_strings[7]
    else:
        execute_time = args[-1]
    msg.x, msg.y, msg.vx, msg.vy, msg.ax, msg.ay, msg.t = args 
    return msg, float(execute_time)
    



def run_tests(test_files):
    testing_node = Node("path_testing")
    path_publisher = testing_node.create_publisher(NextPath, "PATH", 1)
    # log_publisher =  Node.create_publisher(String, "LOG")
    tests = {}
    for test_file in test_files:
        with open(test_file, r"r") as f:
            lines = f.readlines()
            tests[test_file] = [parse_line(l) for l in lines if l!='']

    # start_time =  rclpy.
    for test_file in test_files:
        print("Running test {}".format(test_file))
        for line in tests[test_file]:
            msg, execute_time = line
            path_publisher.publish(msg)
            time.sleep(execute_time-1/1000)


        




def main(args=None):
    rclpy.init()
    if  __name__ == '__main__':
        test_files = None if len(args)==1 else args[1:]

    else:
        test_files = args

    if test_files is None:
        print("No test files given. Running default test")
        test_files = [default_test]

    run_tests(test_files)




if __name__  == '__main__':
    args = sys.argv
    main(args)