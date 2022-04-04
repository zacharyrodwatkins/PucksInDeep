from heapq import _heapify_max
import cv2
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt

class  calibrate_hsv_obj:

    def __init__(self,frame) -> None:
        self.pts = []
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # directory of this python file
        self.frame = frame
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # directory of this python file

        with open(self.dir_path + '/../camera_calib.pkl', 'rb') as f:
            self.from_corners = pickle.load(f)
            
        print(self.from_corners)
        

        self.y_dist = 40+13.0/16
        self.x_dist = 30+13.0/16
        self.des_image_shape = [int(500*self.x_dist/self.y_dist), 500]
        self.pixels_to_cm = self.y_dist*2.54/500
        self.to_corners = [[0,self.des_image_shape[1]], [0,0], [self.des_image_shape[0],0], self.des_image_shape]

        self.transform_matrix = cv2.getPerspectiveTransform(np.float32(self.from_corners), np.float32(self.to_corners))


    def get_corners(self, event, x, y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            print(x,y)
            self.pts.append(np.array([x,y]))

    def calibrate(self):
        self.center = self.pts[0]
        self.radius = np.linalg.norm(self.pts[0]-self.pts[1])
        self.mask = np.zeros(self.frame.shape,dtype=np.uint8)
        self.mask = cv2.circle(self.mask, self.center,int(self.radius),(255,255,255),-1)
        masked_img = cv2.bitwise_and(self.frame,self.mask)
        # plt.imshow(masked_img)
        # plt.show()

        hsv_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2HSV)
        vals = hsv_img[hsv_img[:,:,0]!=0]
        h,s,v = (vals[:,i] for i in range(3))
        for val,label in zip((h,s,v),("h",'s','v')):
            plt.hist(val, label=label,bins=100)
        plt.legend()
        plt.show()

        cut = cv2.inRange(hsv_img, (min(h),min(s),min(v)),(max(h),max(s),max(v)))
        plt.imshow(cut)

        return (min(h), max(h), min(s),max(s), min(v),max(v))




vid = cv2.VideoCapture('udp://10.42.0.1:5000?overrun_nonfatal=1')
vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','4','6'))
frame = vid.read()[1]

for i in range(90):
    frame = vid.read()[1]
# frame = cv2.imread('testFrame.png')

calib = calibrate_hsv_obj(None)
# frame = cv2.warpPerspective(frame, calib.transform_matrix, calib.des_image_shape)
calib.frame = frame

cv2.imwrite("testFrame.png", frame)

cv2.imshow("initialization", frame)


cv2.setMouseCallback("initialization", calib.get_corners)

while (len(calib.pts) < 2):
    cv2.waitKey(1)
# calib.pts = [np.array((154, 229)),
# np.array((167, 228))]

print(calib.calibrate())

cv2.destroyWindow("initialization")