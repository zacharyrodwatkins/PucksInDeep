import socket
import time
import rclpy
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus

class PuckPublisher(Node):

    def __init__(self):
        super().__init__('puck_publisher')

        self.localIP     = "10.42.0.1"
        self.localPort   = 20001
        self.bufferSize  = 1024
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        # Bind to address and ip
        self.UDPServerSocket.bind((self.localIP, self.localPort))
        print("UDP server up and listening")


        self.publisher_ = self.create_publisher(PuckStatus, 'PUCK', 10)

        self.publisher_callback()

    def publisher_callback(self):
        # Listen for incoming datagrams
        while(True):
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)

            message = bytesAddressPair[0]
            address = bytesAddressPair[1]
      
            vals = message.decode()
            vals = vals.split(" ")
            
            vals = [float(x) for x in vals]


            msg = PuckStatus()
            msg.x = vals[0]
            msg.y = vals[1]
            msg.x_vel = vals[2]
            msg.y_vel = vals[3]

            # print('pos: %f , %f     vel: %f . %f' % (msg.x, msg.y, msg.x_vel, msg.y_vel))
            self.publisher_.publish(msg)
         

    

def main(args=None):
    rclpy.init(args=args)

    puck_publisher = PuckPublisher()

    rclpy.spin(puck_publisher)
  
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)\
    puck_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
