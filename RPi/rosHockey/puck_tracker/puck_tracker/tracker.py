from decimal import DivisionByZero
import cv2
import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus
import keyboard
import numpy as np

class PuckTracker(Node):

    def __init__(self):
        super().__init__('puck_tracker')
        self.TL_code = "f u ashley"
        self.TR_code = "lick by butt"
        self.BL_code = "bush did 9/11"
        self.BR_code = "miti 4 president"
        self.puck_pos = [None, None]
        self.puck_vel = [None, None]

        self.vid = cv2.VideoCapture('/dev/v4l/by-path/pci-0000:00:14.0-usb-0:1.1.2:1.0-video-index0')
        self.frame = self.vid.read()[1]
        self.w = self.frame.shape[0]
        self.h = self.frame.shape[1]
        self.left = self.frame[0:int(self.w/2)]
        self.right = self.frame[int(self.w/2):-1]
        self.bboxes = {"tr":[],"tl":[],"bl":[],"br":[]}
        # self.bbox_list = [[],[],[],[]]
        self.decoded_qrs = ['','','','']
        self.qrDecoder = cv2.QRCodeDetector()

        self.initialize()
        # # Puck status updater and display
        # self.frame_rate = 30
        # self.pos_update_period = 1/self.frame_rate
        # self.last_frame_time = time.time()
        # self.pos_timer = self.create_timer(self.pos_update_period, self.update_puck_status)
        # self.QR_timer = self.create_timer(self.pos_update_period, self.get_QR_boxes)
        # self.disp_timer = self.create_timer(self.pos_update_period, self.display)

        # # Puck status publisher
        # self.publisher_ = self.create_publisher(PuckStatus, 'puck_status', 10)
        # publisher_period = 0.01  # seconds
        # self.pub_timer = self.create_timer(publisher_period, self.publish_callback)

        # self.img_array = []
    
    def initialize(self):
        while not (self.decoded_qrs.count('') == 0):
            self.frame = self.vid.read()[1]

            # self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGGR2GRAY)
            # self.frame = cv2.threshold(self.frame, 20, 255, cv2.THRESH_BINARY)

            self.get_QR_boxes()
            print(self.bboxes)
            self.display()
        
        # Used decoded QR text to identify each box as top left, bottom left, etc.
        # for i in range(len(self.decoded_qrs)):
        #     if self.decoded_qrs[i] == self.TR_code:
        #         tr_box = self.bbox_list[i]
        #     elif self.decoded_qrs[i] == self.TL_code:
        #         tl_box = self.bbox_list[i]
        #     elif self.decoded_qrs[i] == self.BR_code:
        #         br_box = self.bbox_list[i]
        #     elif self.decoded_qrs[i] == self.BL_code:
        #         bl_box = self.bbox_list[i]
        
        # Get outermost corners from QR bboxes
        outer_corners = []
        for box in self.bboxes.values():
            max_cent_dist = 0
            print("new box")
            for corner in box:
                dist_from_center = ((corner[0]-self.h/2)**2 + (corner[1]-self.w/2)**2)**(1/2)
                print("center: {}    corner: {}     dist: {}".format([self.h/2, self.w/2], corner, dist_from_center))
                if dist_from_center > max_cent_dist:
                    max_cent_dist = dist_from_center
                    out = corner
            outer_corners.append(out)

        cv2.polylines(self.frame, np.array([outer_corners], np.int32), True, (255,0,0), 3)
        self.display()
        


    def display(self):
        # Put QR bboxes in frame
        # if not (len(self.bbox_list) == 0):
        print("decoded: {}".format(self.decoded_qrs))
        n = 4-self.decoded_qrs.count('')
        print("found {} codes".format(n))
        for bbox in self.bboxes.values():  # For every bounding box
            if bbox is not None:
                cv2.polylines(self.frame, np.array([bbox], np.int32), True, (255,0,0), 3)
                # for j in range(len(bbox)):  # For every corner in the bounding box
                #     cv2.line(self.frame, tuple([int(x) for x in bbox[j]]), tuple([int(x) for x in bbox[(j+1) % len(bbox)]]), (255,0,0), 3)

        if (self.puck_vel[0] is not None):
            self.frame = cv2.putText(self.frame, "x: {} y: {}".format(self.puck_pos[0], self.puck_pos[1]), (0,10), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            self.frame = cv2.putText(self.frame, "x_vel: {} y_vel: {}".format(self.puck_vel[0], self.puck_vel[1]), (0,30), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            cv2.circle(self.frame, (int(self.puck_pos[0]), int(self.puck_pos[1])), 5, (255, 255, 255), -1)

        cv2.imshow('frame', self.frame)

        # If you hit q, stop displaying frame
        # If you hit d, resume displaying frame
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            self.show_frame = False
            cv2.destroyWindow('frame')
        # elif keyboard.is_pressed('d'):
        #     self.show_frame = True

        # if (self.show_frame):
        #     cv2.imshow('frame', self.frame)
    
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
        time_stamp = time.time()

        bin_img = self.filter_for_puck()

        # Use moment to find center of puck from binary image
        try:
            M = cv2.moments(bin_img)
            cX = float(M["m10"] / M["m00"])
            cY = float(M["m01"] / M["m00"])
        except ZeroDivisionError:
            print("lost puck")
            cX = self.puck_pos[0]
            cY = self.puck_pos[1]

        if (self.puck_pos[0] is not None):
            self.puck_vel = [(self.puck_pos[0] - cX)/(time_stamp - self.last_frame_time),
                            (self.puck_pos[1] - cY)/(time_stamp - self.last_frame_time)]

        self.puck_pos = [cX, cY]
        self.last_frame_time = time_stamp

    def get_QR_boxes(self):
        # left = self.frame[0:int(self.w/2)]
        # right = self.frame[int(self.w/2):]
        bottom_left = self.frame[0:int(self.w/2),0:int(self.h/2)]
        top_left = self.frame[0:int(self.w/2),int(self.h/2):]
        top_right = self.frame[int(self.w/2):,int(self.h/2):]
        bottom_right = self.frame[int(self.w/2):,0:int(self.h/2)]

        decoded_bl, bbox_bl, rectified_image_bl = self.qrDecoder.detectAndDecode(bottom_left)
        try:
            self.bboxes["bl"] = bbox_bl[0]
        except TypeError:
            self.bboxes["bl"] = None
        self.decoded_qrs[0] = decoded_bl

        decoded_tl, bbox_tl, rectified_image_tl = self.qrDecoder.detectAndDecode(top_left)
        try:
            self.bboxes["tl"] = [[corner[0]+int(self.h/2), corner[1]] for corner in bbox_tl[0]]
        except TypeError:
            self.bboxes["tl"] = None
        self.decoded_qrs[1] = decoded_tl

        decoded_tr, bbox_tr, rectified_image_tr = self.qrDecoder.detectAndDecode(top_right)
        try:
            self.bboxes["tr"] = [[edge[0]+int(self.h/2), edge[1]+int(self.w/2)] for edge in bbox_tr[0]]
        except TypeError:
            self.bboxes["tr"] = None
        self.decoded_qrs[2] = decoded_tr

        decoded_br, bbox_br, rectified_image_br = self.qrDecoder.detectAndDecode(bottom_right)
        try:
            self.bboxes["br"] = [[edge[0], edge[1]+int(self.w/2)] for edge in bbox_br[0]]
        except TypeError:
            self.bboxes["br"] = None
        self.decoded_qrs[3] = decoded_br
            # print(self.qrDecoder.decodeMulti(left, bboxes_left))
            # self.decoded_qrs[0:2] = self.qrDecoder.decodeMulti(left, bboxes_left)[1]
            # print("left decoded: {}".format(self.decoded_qrs[0:2]))
            # print("top left decoded: {}".format(decoded_tl))
            # self.decoded_qrs[0] = decoded_tl
            # self.bbox_list[0] = bboxes_tl
        # else:
        #     self.decoded_qrs[0:2] = ['','']
        #     self.bbox_list[0:2] = [[],[]]
        #     print("Could not detect both left QR codes")

        # success_right, decoded_right, bboxes_right, rectified_images_right = self.qrDecoder.detectAndDecodeMulti(right)
        # if success_right and (len(bboxes_right) == 2):
        #     print("right decoded: {}".format(decoded_right))
        #     bboxes_right = np.array([[[edge[0], edge[1]+int(self.w/2)] for edge in box] for box in bboxes_right], np.float32)
        #     self.decoded_qrs[2:-1] = decoded_right
        #     self.bbox_list[2:-1] = bboxes_right
        # else:
        #     self.decoded_qrs[2:-1] = ['','']
        #     self.bbox_list[2:-1] = [[],[]]
        #     print("Could not detect both right QR codes")

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