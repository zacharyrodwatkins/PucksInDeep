import cv2
import numpy as np
import pickle
import os

class  calibrate_obj:

    def __init__(self) -> None:
        self.from_corners = []
        self.dir_path = os.path.dirname(os.path.realpath(__file__))  # directory of this python file


    def get_corners(self, event, x, y, flags, param):
        if (event == cv2.EVENT_LBUTTONDOWN):
            print(x,y)
            self.from_corners.append([x,y])


calib = calibrate_obj()

# os.system('ssh pi@10.42.0.124 "~/run_camera_to_laptop.bash" &')
vid = cv2.VideoCapture('udp://10.42.0.1:5000?overrun_nonfatal=1')
vid.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','4','6'))



frame = vid.read()[1]
cv2.imshow("initialization", frame)



cv2.setMouseCallback("initialization", calib.get_corners)
while (len(calib.from_corners) < 4):
    cv2.waitKey(1)
cv2.destroyWindow("initialization")


with open(calib.dir_path + '/../calibration/camera_calib.txt', 'w') as f:
    for i in range(len(calib.from_corners)):
        f.write("{} {}".format(calib.from_corners[i][0],calib.from_corners[i][1]))
        if (i<len(calib.from_corners)-1):
            f.write("\n")