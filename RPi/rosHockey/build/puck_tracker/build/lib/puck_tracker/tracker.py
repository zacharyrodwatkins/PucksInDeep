from decimal import DivisionByZero
import cv2
import rclpy
import time
from rclpy.node import Node
from hockey_msgs.msg import PuckStatus

class PuckTracker(Node):

    def __init__(self):
        super().__init__('puck_tracker')
        self.puck_pos = [None, None]
        self.puck_vel = [None, None]

        self.vid = cv2.VideoCapture('/dev/video0')
        self.frame_rate = 30
        self.pos_update_period = 1/self.frame_rate
        self.last_frame_time = time.time()
        self.pos_timer = self.create_timer(self.pos_update_period, self.update_puck_status)
        # self.i = 0

        self.publisher_ = self.create_publisher(PuckStatus, 'puck_status', 10)
        publisher_period = 0.01  # seconds
        self.pub_timer = self.create_timer(publisher_period, self.publish_callback)

        self.img_array = []

    def publish_callback(self):
        if self.puck_vel[0] is not None:
            msg = PuckStatus()
            msg.x = self.puck_pos[0]
            msg.y = self.puck_pos[1]
            msg.x_vel = self.puck_vel[0]
            msg.y_vel = self.puck_vel[1]
            self.publisher_.publish(msg)
            print('pos: %f , %f     vel: %f . %f' % (msg.x, msg.y, msg.x_vel, msg.y_vel))

    def update_puck_status(self):
        # Capture the video frame and record time of frame
        ret, frame = self.vid.read()
        # frame = cv2.resize(frame, (640, 480))       
        time_stamp = time.time()
        # self.i += 1

        # Convert to HSV and filter to binary image for puck isolation
        # Red puck has hue on boundary between 0 and 180, so two filters are used and summed
        hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv_min = (0, int(0.6*255), int(0.20*255))
        hsv_max = (8, int(0.98*255), int(0.80*255))
        low_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        hsv_min = (175, int(0.6*255), int(0.40*255))
        hsv_max = (180, int(0.98*255), int(0.80*255))
        high_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
        bin_img = low_hue_bin_img + high_hue_bin_img

        # Use moment to find center of puck from binary image
        try:
            M = cv2.moments(bin_img)
            cX = float(M["m10"] / M["m00"])
            cY = float(M["m01"] / M["m00"])
        except DivisionByZero:
            print("lost puck")
            cX = self.puck_pos[0]
            cY = self.puck_pos[1]

        if (self.puck_pos[0] is not None):
            self.puck_vel = [(self.puck_pos[0] - cX)/(time_stamp - self.last_frame_time),
                            (self.puck_pos[1] - cY)/(time_stamp - self.last_frame_time)]
            frame = cv2.putText(frame, "x: {} y: {}".format(cX, cY), (0,10), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            frame = cv2.putText(frame, "x_vel: {} y_vel: {}".format(self.puck_vel[0], self.puck_vel[1]), (0,30), cv2.FONT_HERSHEY_SIMPLEX, .4, (0,0,0), 1, cv2.LINE_AA)
            cv2.circle(frame, (int(cX), int(cY)), 5, (255, 255, 255), -1)

        self.puck_pos = [cX, cY]
        self.last_frame_time = time_stamp
        self.img_array.append(frame)


def main(args=None):
    rclpy.init(args=args)

    puck_tracker = PuckTracker()

    try:
        rclpy.spin(puck_tracker)
    except KeyboardInterrupt:
        print("saving video")
        i = 0
        for f in puck_tracker.img_array:
            padding = "0" * (10 - len(str(i)))
            cv2.imwrite("/home/ubuntu/PucksInDeep/RPi/rosHockey/puck_tracker/recording/" + padding + str(i) + ".jpg", f) 
            i += 1

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