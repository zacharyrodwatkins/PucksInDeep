import cv2
import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus, NextPath
from std_msgs.msg import String
import numpy as np
import pickle
import os 
import datetime
from scipy.signal import savgol_filter 

class PuckTracker(Node):

    def __init__(self):
        super().__init__('puck_tracker')
        self.index = 1
        self.puck_pos = [None, None]
        self.puck_vel = [None, None]

        # Initialization parameters for perspective transform
        self.y_dist = 40+13.0/16
        self.x_dist = 30+13.0/16
        self.des_image_shape = [int(1000*self.x_dist/self.y_dist), 1000]
        self.pixels_to_cm = self.y_dist*2.54/1000
        self.from_corners = []
        self.to_corners = [[0,self.des_image_shape[1]], [0,0], [self.des_image_shape[0],0], self.des_image_shape]

        # Setup video capture and recording objects
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # directory of this python file
        # ls /dev/v4l/by-path then mash tab and take an index 0 careful not to take webcam
        # self.vid = cv2.VideoCapture('/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.4:1.0-video-index0')
        
        os.system('ssh pi@10.42.0.124 "~/run_camera.bash" &')
        self.vid = cv2.VideoCapture('udp://10.42.0.1:5000')
        self.vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','4','6'))
        self.frame = self.vid.read()[1]
        self.w = self.frame.shape[0]
        self.h = self.frame.shape[1]
        
        # Run camera initialization
        self.initialize()

        # Puck status updater and display
        self.frame_rate = 120
        self.pos_update_period = 1.0/self.frame_rate
        self.last_frame_time = time.time()  # seconds
        self.show_frame = False
        self.SG_window = 7
        self.SV_poly_order = 4
        self.xvel_buffer = [0]*self.SG_window
        self.yvel_buffer = [0]*self.SG_window
        self.pos_timer = self.create_timer(self.pos_update_period, self.update_puck_status)


        self.publisher_ = self.create_publisher(PuckStatus, 'PUCK', 10)
        self.path_flag = True
        self.path_subscriber = self.create_subscription(NextPath, 'PATH', self.path_cb, 10)
        self.flag = True
        self.flag_subscriber = self.create_subscription(String, 'FLAG', self.bp_cb, 10)
        self.bp_flag = True
        self.found = 0

        self.path_publisher = self.create_publisher(NextPath,'PATH',10)

    def path_cb(self,args):
        self.path_flag = False
        self.get_logger().info("green dot")

    def bp_cb(self,args):
        print("bitch")
        self.bp_flag = False

    def initialize(self):
        recal = input("Recalibrate camera? (y/N)\n")
        rec = input("Record video? (y/N)")
        
        self.record = False
        if rec in ['y', 'Y']:
            self.vid_out = cv2.VideoWriter(self.dir_path + '/../videos/' + str(datetime.datetime.now()) + '.avi',
                                             cv2.VideoWriter_fourcc(*'MP42'), 30.0, self.des_image_shape)
            self.record = True

        if recal in ['y', 'Y']:
            self.frame = self.vid.read()[1]
            cv2.imshow("initialization", self.frame)
            cv2.setMouseCallback("initialization", self.get_corners)
            while (len(self.from_corners) < 4):
                cv2.waitKey(1)
            cv2.destroyWindow("initialization")
            with open(self.dir_path + '/../camera_calib.pkl', 'wb') as f:
                pickle.dump(self.from_corners, f)

        else:
            with open(self.dir_path + '/../camera_calib.pkl', 'rb') as f:
                self.from_corners = pickle.load(f)
            
        
        
        self.transform_matrix = cv2.getPerspectiveTransform(np.float32(self.from_corners), np.float32(self.to_corners))
        
        # os.system("v4l2-ctl -d /dev/video0 --set-ctrl=exposure_auto=1")
        # os.system("v4l2-ctl -d /dev/video0 --set-ctrl=exposure_absolute=60")


    def get_corners(self, event, x, y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            print(x,y)
            self.from_corners.append([x,y])


    def display(self):

        if not self.show_frame and self.record:
            if self.puck_vel[0] is not None:
                self.frame = cv2.putText(self.frame, "x: {:.2f} y: {:.2f}".format(self.puck_pos[0], self.puck_pos[1]),
                                            (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                self.frame = cv2.putText(self.frame, "x_vel: {:.2f} y_vel: {:.2f}".format(self.puck_vel[0], self.puck_vel[1]),
                                            (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
                cv2.circle(self.frame, (int(self.puck_pos[0]/self.pixels_to_cm), int(self.des_image_shape[1] - self.puck_pos[1]/self.pixels_to_cm)),
                                            5, (255, 255, 255), -1)
            if not self.flag:
                cv2.circle(self.frame , (self.frame.shape[1]-10, self.frame.shape[1]-10), 5, (255,0,0), -1)

            if not self.path_flag:
                # self.path_flag = True
                cv2.circle(self.frame, (self.frame.shape[1]-10, self.frame.shape[1]-5), 5, (0,255,0), -1)

            if not self.bp_flag:
                cv2.circle(self.frame, (self.frame.shape[1]-10, self.frame.shape[1]-0), 5, (255,0,255), -1)

            self.vid_out.write(self.frame)

            

        if (self.puck_vel[0] is not None):
            self.frame = cv2.putText(self.frame, "x: {:.2f} y: {:.2f}".format(self.puck_pos[0], self.puck_pos[1]),
                                        (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
            self.frame = cv2.putText(self.frame, "x_vel: {:.2f} y_vel: {:.2f}".format(self.puck_vel[0], self.puck_vel[1]),
                                        (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)

            cv2.circle(self.frame, (int(self.puck_pos[0]/self.pixels_to_cm), int(self.des_image_shape[1] - self.puck_pos[1]/self.pixels_to_cm)),
                                        5, (255, 255, 255), -1)

        # If you hit q, stop displaying frame
        # If you hit d, resume display
        # elif cv2.waitKey(1) & 0xFF == ord('d'):
        #     self.show_frame = Trueing frame
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            self.show_frame = False
            if self.record:
                self.vid_out.release()
            cv2.destroyWindow('frame')

        if (self.show_frame):
            if self.record:
                self.vid_out.write(self.frame)
            cv2.imshow('frame', self.frame)

    def publish_callback(self):
        if self.puck_vel[0] is not None:
            self.index = self.index + 1
            msg = PuckStatus()
            msg.x = self.puck_pos[0]
            msg.y = self.puck_pos[1]
            msg.x_vel = self.puck_vel[0]
            msg.y_vel = self.puck_vel[1]
            # self.get_logger().info("publish callback vel {}".format(msg.y_vel))
            print('pos: %f , %f     vel: %f . %f' % (msg.x, msg.y, msg.x_vel, msg.y_vel))
            self.publisher_.publish(msg)

    def update_puck_status(self):
        self.get_logger().info("display start")
        self.display()
        # self.get_logger().info("display end")
        # self.get_logger().info("start update status")
        # Capture the video frame and record time of frame
        ret, self.frame = self.vid.read()
        self.frame = cv2.warpPerspective(self.frame, self.transform_matrix, self.des_image_shape)
        time_stamp = time.time()  # seconds

        bin_img = self.filter_for_puck()

        # Use moment to find center of puck from binary image
        try:
            M = cv2.moments(bin_img)
            if(M["m00"]<100000):
                M["m00"] = 0
            cX = float(M["m10"] / M["m00"]) * self.pixels_to_cm
            cY = (self.des_image_shape[1] - float(M["m01"] / M["m00"])) * self.pixels_to_cm  # Subtracting from image height to get y=0 at bottom
            self.found = 0
        except ZeroDivisionError:
            self.found = self.found+1
            print("lost puck")
            if self.found>2:
                # if puck is lost for more than 3 frames then publish lost puck
                cX = -1.0
                cY = -1.0
            else:
                cX = self.puck_pos[0]
                cY = self.puck_pos[1]


        if (self.puck_pos[0] is not None):
            # load new x and y velocities into buffer, and apply savgol filter to smooth noise
            del self.xvel_buffer[0]
            self.xvel_buffer.append((cX - self.puck_pos[0])/(time_stamp - self.last_frame_time))
            del self.yvel_buffer[0]
            self.yvel_buffer.append((cY - self.puck_pos[1])/(time_stamp - self.last_frame_time))
            xvel_filtered = savgol_filter(self.xvel_buffer, self.SG_window, self.SV_poly_order)
            yvel_filtered = savgol_filter(self.yvel_buffer, self.SG_window, self.SV_poly_order)
            self.puck_vel = [xvel_filtered[-1], yvel_filtered[-1]]

            # raw_xvel = (cX - self.puck_pos[0])/(time_stamp - self.last_frame_time)
            # raw_yvel = (cY - self.puck_pos[1])/(time_stamp - self.last_frame_time)

            if (yvel_filtered[-1]<-150):
                if (self.flag == True):
                    self.flag = False
                    msg = NextPath()
                    msg.x = 9.0
                    msg.y = 30.0
                    msg.vx = 0.0
                    msg.vy = 0.0
                    msg.ax = 0.0
                    msg.ay = 0.0
                    msg.t = 1.0
                    # self.path_publisher.publish(msg)
            #         self.get_logger().info("puck pos: {} {}".format(cX,cY))
            # self.puck_vel = [raw_xvel, raw_yvel]

        self.puck_pos = [cX, cY]
        self.last_frame_time = time_stamp
        # self.get_logger().info("publish start")
        self.publish_callback()
        # self.get_logger().info("publish end")
        # self.get_logger().info("end update status")

    def filter_for_puck(self):
        # Convert to HSV and filter to binary image for puck isolation
        # Red puck has hue on boundary between 0 and 180, so two filters are used and summed
        hsv_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        # hsv_min = (0, int(0.3*255), int(0.20*255))
        # hsv_max = (15, int(0.98*255), int(0.80*255))
        hsv_min = (0, 0.70*255, 0.06*255)
        hsv_max = (19, 1.00*255, 0.12*255)
        low_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        # hsv_min = (175, int(0.3*255), int(0.20*255))
        # hsv_max = (180, int(0.98*255), int(0.80*255))
        hsv_min = (170, 0.7*255, 0.06*255)
        hsv_max = (180, 1.0*255, 0.12*255)
        high_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        bin_img = low_hue_bin_img + high_hue_bin_img
        # cv2.imshow("low", low_hue_bin_img)
        # cv2.imshow("high", high_hue_bin_img)
        return bin_img

def main(args=None):
    rclpy.init(args=args)

    puck_tracker = PuckTracker()

    try:
        rclpy.spin(puck_tracker)
    except KeyboardInterrupt:
        print("closing video writer")
        puck_tracker.vid.release()

        # i = 0
        # for f in puck_tracker.img_array:
        #     padding = "0" * (10 - len(str(i)))
        #     cv2.imwrite("/home/ubuntu/PucksInDeep/RPi/rosHockey/puck_tracker/recording/" + padding + str(i) + ".jpg", f) 
        #     i += 1

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)\
    puck_tracker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
