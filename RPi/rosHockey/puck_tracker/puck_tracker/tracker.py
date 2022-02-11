from decimal import DivisionByZero
import queue
import cv2
import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus
import keyboard
import numpy as np
import pickle

class PuckTracker(Node):

    def __init__(self):
        super().__init__('puck_tracker')
        self.puck_pos = [None, None]
        self.puck_vel = [None, None]

        self.vid = cv2.VideoCapture('/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1.2:1.0-video-index0')
        self.frame = self.vid.read()[1]
        self.w = self.frame.shape[0]
        self.h = self.frame.shape[1]
        
        # Initialization parameters for perspective transform
        self.y_dist = 40+13.0/16
        self.x_dist = 30+13.0/16
        self.des_image_shape = [int(1000*self.x_dist/self.y_dist), 1000]
        self.pixels_to_cm = self.y_dist*2.54/1000
        self.from_corners = []
        self.to_corners = [[0,self.des_image_shape[1]], [0,0], [self.des_image_shape[0],0], self.des_image_shape]
        self.initialize()

        # Puck status updater and display
        self.frame_rate = 30
        self.pos_update_period = 1/self.frame_rate
        self.last_frame_time = time.time()
        self.show_frame = True
        self.pos_timer = self.create_timer(self.pos_update_period, self.update_puck_status)
        self.disp_timer = self.create_timer(self.pos_update_period, self.display)

        # # Puck status publisher(self.frame.shape[1], self.frame.shape[0]
        # self.publisher_ = self.create_publisher(PuckStatus, 'puck_status', 10)
        # publisher_period = 0.01  # seconds
        # self.pub_timer = self.create_timer(publisher_period, self.publish_callback)

        # self.img_array = []
    
    def initialize(self):
        recal = input("Recalibrate camera? (Y/n)\n")

        if recal in ['y', 'Y', '']:
            self.frame = self.vid.read()[1]
            cv2.imshow("initialization", self.frame)
            cv2.setMouseCallback("initialization", self.get_corners)
            while (len(self.from_corners) < 4):
                cv2.waitKey(1)
            cv2.destroyWindow("initialization")
            with open('camera_calib.pkl', 'wb') as f:
                pickle.dump(self.from_corners, f)

        else:
            with open('camera_calib.pkl', 'rb') as f:
                self.from_corners = pickle.load(f)
            
        
        self.transform_matrix = cv2.getPerspectiveTransform(np.float32(self.from_corners), np.float32(self.to_corners))

    def get_corners(self, event, x, y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            print(x,y)
            self.from_corners.append([x,y])


    def display(self):
        if (self.puck_vel[0] is not None):
            self.frame = cv2.putText(self.frame, "x: {} y: {}".format(self.puck_pos[0], self.puck_pos[1]), (0,10), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            self.frame = cv2.putText(self.frame, "x_vel: {} y_vel: {}".format(self.puck_vel[0], self.puck_vel[1]), (0,30), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            cv2.circle(self.frame, (int(self.puck_pos[0]/self.pixels_to_cm), int(self.puck_pos[1]/self.pixels_to_cm)), 5, (255, 255, 255), -1)

        # cv2.imshow('frame', self.frame)

        # If you hit q, stop displaying frame
        # If you hit d, resume displaying frame
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            self.show_frame = False
            cv2.destroyWindow('frame')
        # elif cv2.waitKey(1) & 0xFF == ord('d'):
        #     self.show_frame = True

        if (self.show_frame):
            cv2.imshow('frame', self.frame)
    
    def publish_callback(self):
        if self.puck_vel[0] is not None:
            msg = PuckStatus()
            msg.x = self.puck_pos[0]
            msg.y = self.puck_pos[1]
            msg.x_vel = self.puck_vel[0]
            msg.y_vel = self.puck_vel[1]
            self.publisher_.publish(msg)
            # print('pos: %f , %f     vel: %f . %f' % (msg.x, msg.y, msg.x_vel, msg.y_vel))

    def update_puck_status(self):
        # Capture the video frame and record time of frame
        ret, self.frame = self.vid.read()
        self.frame = cv2.warpPerspective(self.frame, self.transform_matrix, self.des_image_shape)
        time_stamp = time.time()

        bin_img = self.filter_for_puck()

        # Use moment to find center of puck from binary image
        try:
            M = cv2.moments(bin_img)
            cX = float(M["m10"] / M["m00"]) * self.pixels_to_cm
            cY = float(M["m01"] / M["m00"]) * self.pixels_to_cm
        except ZeroDivisionError:
            print("lost puck")
            cX = self.puck_pos[0]
            cY = self.puck_pos[1]

        if (self.puck_pos[0] is not None):
            self.puck_vel = [(self.puck_pos[0] - cX)/(time_stamp - self.last_frame_time),
                            (self.puck_pos[1] - cY)/(time_stamp - self.last_frame_time)]

        self.puck_pos = [cX, cY]
        self.last_frame_time = time_stamp

    def filter_for_puck(self):
        # Convert to HSV and filter to binary image for puck isolation
        # Red puck has hue on boundary between 0 and 180, so two filters are used and summed
        hsv_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        hsv_min = (0, int(0.6*255), int(0.20*255))
        hsv_max = (8, int(0.98*255), int(0.80*255))
        low_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        hsv_min = (175, int(0.6*255), int(0.40*255))
        hsv_max = (180, int(0.98*255), int(0.80*255))
        high_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        bin_img = low_hue_bin_img + high_hue_bin_img

        return bin_img

def main(args=None):
    rclpy.init(args=args)

    puck_tracker = PuckTracker()

    try:
        rclpy.spin(puck_tracker)
    except KeyboardInterrupt:
        print("saving video")
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

# define a video capture object
# vid = cv2.VideoCapture(0)
# # vid_out = cv2.VideoWriter('/home/ubuntu/PucksInDeep/RPi/rosHockey/001.avi', cv2.VideoWriter_fourcc(*'MP42'), 30.0, (640,480))
# i = 0
# while(True):
      
#     # Capture the video frame
#     ret, frame = vid.read()
#     if not ret:
#         break
#     hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     hsv_min = (0, int(0.6*255), int(0.20*255))
#     hsv_max = (8, int(0.98*255), int(0.80*255))
#     low_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
#     hsv_min = (175, int(0.6*255), int(0.40*255))
#     hsv_max = (180, int(0.98*255), int(0.80*255))
#     high_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
#     bin_img = low_hue_bin_img + high_hue_bin_img
#     binvert = cv2.bitwise_not(bin_img)
#     M = cv2.moments(bin_img)
#     cX = int(M["m10"] / M["m00"])
#     cY = int(M["m01"] / M["m00"])
    


#     cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
#     # Display the resulting frames
#     cv2.imshow('bin', frame)



#     # cv2.imshow('inv', binvert)
#     # cv2.imshow('low', low_hue_bin_img)
#     # cv2.imshow('high', high_hue_bin_img)
#     # cv2.imshow('frame', frame)  
    
#     # the 'q' button is set as the
#     # quitting button you may use any
#     # desired button of your choice
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#     i += 1
  
# # After the loop release the cap object
# vid.release()
# # vid_out.release()
# # Destroy all the windows
# cv2.destroyAllWindows()