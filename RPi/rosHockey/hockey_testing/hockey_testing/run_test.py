import rclpy
import sys
from hockey_msgs.msg import NextPath
default_test = "test_files/default.txt"


def parse_line(line):
    msg = NextPath()
    args  = [float(s) for s in line.split()[:8]]
    msg.x, msg.y, msg.vx, msg.vy, msg.ax, msg.ay, msg.t = args 
    return msg

    

def run_tests(test_files):
    path_publisher = rclpy.Node.create_publisher(NextPath, "PATH")
    tests = {}
    for test_file in test_files:
        with open(test_file, r"r") as f:
            lines = f.readlines()
            tests[test_file] = [parse_line(l) for l in lines]

    # start_time =  rclpy.
    for test in test_files:
        print("Running test")

        




def main(args=None):
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