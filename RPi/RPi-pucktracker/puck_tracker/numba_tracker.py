import time
import numpy as np
import pickle
import os 
import datetime
from scipy.signal import savgol_filter 
import cv2
# import matplotlib.pyplot as plt
import socket
from numba import jit

#night man
#oh wooooahhhhhh

class PuckTracker():

    def __init__(self):

        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # directory of this python file

        self.serverAddressPort   = ("10.42.0.1", 20001)
        self.bufferSize          = 1024
        self.UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        with open(self.dir_path + '/../camera_calib.pkl', 'rb') as f:
            self.from_corners = pickle.load(f)
            
        print(self.from_corners)
        
        self.index = 1
        self.puck_pos = [-1.0, -1.0]
        self.puck_vel = [0.0, 0.0]


        self.show_frame = False
        self.SG_window = 7
        self.SV_poly_order = 4
        self.xvel_buffer = [0]*self.SG_window
        self.yvel_buffer = [0]*self.SG_window

        self.puck_radius =  3
        # print("M00 cut")
        self.y_dist = 640#40+13.0/16
        self.x_dist = 480#30+13.0/16
        self.max_size = 640
        
        self.M00_cut = 0.5*np.pi*(self.puck_radius*self.max_size/self.y_dist)**2
        # print(self.M00_cut)
        
        self.des_image_shape = [int(self.max_size*self.x_dist/self.y_dist), self.max_size]
        self.pixels_to_cm = self.y_dist*2.54/self.max_size
        self.to_corners = [[0,self.des_image_shape[1]], [0,0], [self.des_image_shape[0],0], self.des_image_shape]

        self.transform_matrix = cv2.getPerspectiveTransform(np.float32(self.from_corners), np.float32(self.to_corners))

        print(self.to_corners)
        print(self.from_corners)
        # os.system('ssh pi@10.42.0.124 "~/run_camera_to_laptop.bash"')
        # self.vid = cv2.VideoCapture('udp://10.42.0.124:5000?overrun_nonfatal=1&fifo_size=50000000"')
        # self.vid = cv2.VideoCapture('udp://127.0.0.1:5000?overrun_nonfatal=1&fifo_size=50000000"')
        # self.vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','4','6'))

        # self.frame = self.vid.read()[1]
        # self.frame_green = self.frame[:,:,1]
        # self.w = self.frame.shape[0]
        # self.h = self.frame.shape[1]
        
        self.last_frame_time = time.time()  # seconds

        self.found = 0
        self.tick_tocks = []





    def display(self):
        cv2.imshow("frame", self.frame)
        cvt_image = np.stack((self.bin_image,self.bin_image,self.bin_image),axis=-1)
        cv2.imshow("binary", 255*self.bin_image.astype(np.uint8))
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            cv2.destroyWindow('frame')
            exit()

    

        # if not self.show_frame and self.record:
        #     if self.puck_vel[0] is not None:
        #         self.frame = cv2.putText(self.frame, "x: {:.2f} y: {:.2f}".format(self.puck_pos[0], self.puck_pos[1]),
        #                                     (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        #         self.frame = cv2.putText(self.frame, "x_vel: {:.2f} y_vel: {:.2f}".format(self.puck_vel[0], self.puck_vel[1]),
        #                                     (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)
        #         cv2.circle(self.frame, (int(self.puck_pos[0]/self.pixels_to_cm), int(self.des_image_shape[1] - self.puck_pos[1]/self.pixels_to_cm)),
        #                                     5, (255, 255, 255), -1)
            
        #     self.vid_out.write(self.frame)
        #     return

            

        # if (self.puck_vel[0] is not None):
        #     self.frame = cv2.putText(self.frame, "x: {:.2f} y: {:.2f}".format(self.puck_pos[0], self.puck_pos[1]),
        #                                 (0,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)
        #     self.frame = cv2.putText(self.frame, "x_vel: {:.2f} y_vel: {:.2f}".format(self.puck_vel[0], self.puck_vel[1]),
        #                                 (0,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 1, cv2.LINE_AA)

        #     cv2.circle(self.frame, (int(self.puck_pos[0]/self.pixels_to_cm), int(self.des_image_shape[1] - self.puck_pos[1]/self.pixels_to_cm)),
        #                                 5, (255, 255, 255), -1)


        # if (cv2.waitKey(1) & 0xFF) == ord('q'):
        #     self.show_frame = False
        #     if self.record:
        #         self.vid_out.release()
        #     cv2.destroyWindow('frame')

        # if (self.show_frame):
        #     if self.record:
        #         self.vid_out.write(self.frame)
        #     cv2.imshow('frame', self.frame)

    
    def publish_callback(self):
        print (self.puck_pos, self.puck_vel)

    
    def update_puck_status(self):
        tic1 = time.time()
        tic = time.time_ns()
        ret, frame = self.vid.read()
        tic_pers = time.time()
        # self.frame = cv2.warpPerspective(frame, self.transform_matrix, self.des_image_shape)
        # self.frame = frame
        self.frame_green = frame[:,:,1]
        tock_pers = time.time()
        t_pers = (tock_pers-tic_pers)*1000
        print("t perspective = {}".format(t_pers))
        time_stamp = time.time()

        tic_filt = time.time()
        # bin_img = self.filter_for_puck()
        bin_img = self.filter_g()
        tock_filt = time.time()
        t_filt = (tock_filt-tic_filt)*1000
        print("t filter = {}".format(t_filt))
        self.bin_image = bin_img
        # self.display()

        tic_mom = time.time()
        M = cv2.moments(bin_img)
        # print(M['m00'])
        if(M["m00"]<self.M00_cut):
            M["m00"] = 0
            self.found = self.found+1
            if self.found>2:
            # if puck is lost for more than 3 frames then publish lost puck
                cX = -1.0
                cY = -1.0
            else: # otherwise chill pretend its still where it was
                cX = self.puck_pos[0]
                cY = self.puck_pos[1]


        else:
            cX = float(M["m10"] / M["m00"]) * self.pixels_to_cm
            cY = (self.des_image_shape[1] - float(M["m01"] / M["m00"])) * self.pixels_to_cm  # Subtracting from image height to get y=0 at bottom
            self.found = 0

        tock_mom = time.time()
        t_mom = (tock_mom-tic_mom)*1000
        print("t moment = {}".format(t_mom))


        # if (self.puck_pos[0] is not None):
        #     # load new x and y velocities into buffer, and apply savgol filter to smooth noise
        #     del self.xvel_buffer[0]
        #     self.xvel_buffer.append((cX - self.puck_pos[0])/(time_stamp - self.last_frame_time))
        #     del self.yvel_buffer[0]
        #     self.yvel_buffer.append((cY - self.puck_pos[1])/(time_stamp - self.last_frame_time))
        #     # xvel_filtered = savgol_filter(self.xvel_buffer, self.SG_window, self.SV_poly_order)
        #     # yvel_filtered = savgol_filter(self.yvel_buffer, self.SG_window, self.SV_poly_order)
        #     self.puck_vel = [xvel_filtered[-1], yvel_filtered[-1]]


        self.puck_pos = [cX, cY]
        self.last_frame_time = time_stamp
        self.publish_callback()
        toc = time.time_ns()
        self.tick_tocks.append(toc-tic)
        # print(self.puck_pos, self.puck_vel)
        msg = str.encode("{:.3f} {:.3f} {:.3f} {:.3f}".format(*self.puck_pos, *self.puck_vel))
        self.UDPSocket.sendto(msg, self.serverAddressPort)
        
        tock1 = time.time()
        print((tock1-tic1)*1000)


    def filter_for_puck(self):
        # Convert to HSV and filter to binary image for puck isolation
        
        # Red puck has hue on boundary between 0 and 180, so two filters are used and summed
        tic = time.time_ns()
        hsv_img = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        hsv_min = (0, 80, 130)
        hsv_max = (5, 143, 165)
        low_hue_bin_img = (cv2.inRange(hsv_img, hsv_min, hsv_max)==255)
        hsv_min = (170, 80, 130)
        hsv_max = (181, 143, 165)
        high_hue_bin_img = (cv2.inRange(hsv_img, hsv_min, hsv_max)==255)
        bin_img = (low_hue_bin_img) | (high_hue_bin_img)
        toc = time.time_ns()
        print("done in {}".format((toc-tic)*1e-6))
        return bin_img.astype(np.uint8)
        # # hsv_min = (0, 90, 45)
        # # hsv_max = (180, 140, 80)
        # return cv2.inRange(hsv_img, hsv_min, hsv_max)

    def filter_g(self):
        return (cv2.inRange(self.frame_green,120,255)).astype(np.uint8)

# @jit
def make_bin_img(img):

    tic = time.time_ns()
    # return np.img[:,:,2]/(np.abs(img[:,:,0]-img[:,:,1])+1)
    # R, G, B values are divided by 255
    # to change the range from 0..255 to 0..1:
    # r, g, b = r / 255.0, g / 255.0, b / 255.0
 
    # h, s, v = hue, saturation, value
    cmax = np.max(img, -1)    # maximum of r, g, b
    cmin = np.min(img, -1)  
    diff = cmax-cmin + 1      # diff of cmax and cmin.
 
    bin_img = np.zeros((img.shape[0],img.shape[1]))
    # h = (60 *((img[:,:,1] - img[:,:,0]) * diff+ 120)%360)*((img[:,:,2]==cmax))
    h = (60 *((img[:,:,1] - img[:,:,0])/diff+ 120))%360*((img[:,:,2]==cmax))
    s = diff/cmax*255
    v = cmax
    bin_img[(h<260)&(h>224)&(s>20)&(s<87)&(v<194)&(v>173)]=1
    toc = time.time_ns()
    print("done in {}".format((toc-tic)*1e-6))
    return bin_img#bin_img


    # bin_img = np.zeros(img.shape)
    # bin_img[(cmax == img[:,:,2]) & (diff>40)] = 255
    # return bin_img
    # ok_spots = np.where(cmax == img[:,:,2])

    # if cmax and cmax are equal then h = 0
    if cmax == cmin:
        h = 0
     
    # if cmax equal r then compute h


    elif cmax == img[:,:,2]:
        h = (60 * ((g - b) / diff) + 360) % 360

 
    # if cmax equal g then compute h
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360
 
    # if cmax equal b then compute h
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360
 
    # if cmax equal zero
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100
 
    # compute v
    v = cmax * 100
    return h, s, v
 



def main(args=None):
    puck_tracker = PuckTracker()

    try:
        while(True):
            puck_tracker.update_puck_status()
    except KeyboardInterrupt:
        # close video write
        puck_tracker.vid.release()
        tictocs = np.array(puck_tracker.tick_tocks)
        plt.hist(tictocs/1e6)
        print("Mean: {} ms".format(np.mean(tictocs/1e6)))
        plt.show()
        

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    img = cv2.imread("testFrame.png")
    # bin_img = make_bin_img(img)
    puck_tracker = PuckTracker()
    # puck_tracker.frame = img
    # bin_img = puck_tracker.filter_for_puck()
    bin_img = make_bin_img(img)
    plt.imshow(bin_img)
    plt.show()
    # main()
