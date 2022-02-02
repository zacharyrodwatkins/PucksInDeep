import cv2
import os

directory = '/home/ubuntu/PucksInDeep/RPi/rosHockey/puck_tracker/recording/'
vid_name = 'tracker_check.avi'

images = [img for img in os.listdir(directory) if img.endswith(".jpg")]
images.sort()


# video = cv2.VideoWriter
for image in images:
    frame = cv2.imread(directory + image)
    # height, width, layers = frame.shape
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()