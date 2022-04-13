import socket
import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus
import numpy as np
import matplotlib.pyplot as plt

class PuckPublisher(Node):

    def __init__(self):
        super().__init__('puck_publisher')

        self.publisher_ = self.create_publisher(PuckStatus, 'PUCK', 10)
        self.localIP     = "10.42.0.1"
        self.localPort   = 8080
        self.bufferSize  = 1024
        self.ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ServerSocket.bind((self.localIP, self.localPort))
        self.ServerSocket.listen()
        self.time_stamps = []

        # self.publisher_callback()


    def publisher_callback(self):
        conn, addr = self.ServerSocket.accept()
        with conn:
            while(True):
                message,_ = conn.recvfrom(self.bufferSize)
                vals = message.decode()
                vals = vals.split()
                if len(vals)<4:
                    print("Incomplete message. Exiting")
                    return

                vals = [float(x) for x in vals]
                self.time_stamps.append(time.time_ns())



                msg = PuckStatus()
                msg.x = vals[0]
                msg.y = vals[1]
                msg.x_vel = vals[2]
                msg.y_vel = vals[3]

                # print('pos: %f , %f     vel: %f . %f' % (msg.x, msg.y, msg.x_vel, msg.y_vel))
                self.publisher_.publish(msg)
                if not message:
                    break

         

    

def main(args=None):
    rclpy.init(args=args)

    puck_publisher = PuckPublisher()
    puck_publisher.publisher_callback()
    time_steps = 1e-6*(np.diff(np.array(puck_publisher.time_stamps)))
    print("Average time between message {}".format(1e-6*np.mean(np.diff(np.array(puck_publisher.time_stamps)))))
    plt.hist(time_steps)
    plt.show()
    plt.plot(time_steps)
    plt.show()
    
    # print(puck_publisher.time_stamps)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)\
    puck_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
