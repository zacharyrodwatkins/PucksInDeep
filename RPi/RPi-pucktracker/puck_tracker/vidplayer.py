import cv2
import numpy as np
import os

# os.system('ssh pi@10.42.0.124 "~/run_camera.bash" &')
cap = cv2.VideoCapture('udp://10.42.0.1:5000')
print("here")
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','4','6'))
if not cap.isOpened():
    print('VideoCapture not opened')
    exit(-1)
i = 0

# os.system('ssh pi@10.0.42.124 "~/run_camera.bash" &')
print("here")

while True:
    ret, frame = cap.read()

    if not ret:
        print('frame empty')
        break

    cv2.imshow('Camera Feed', frame)

    if cv2.waitKey(1)&0XFF == ord('q'):
        break

    i+=1
    print(i)
    
t = 10
print(i/t)
cap.release()
cv2.destroyAllWindows()
