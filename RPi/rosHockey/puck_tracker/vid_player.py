import cv2
import os
import time

directory = "C:\\Users\\epham\\Documents\\airhockey\\PucksInDeep\\RPi\\rosHockey\\puck_tracker\\recording\\"

images = [img for img in os.listdir(directory) if img.endswith(".jpg")]
images.sort()
print(images)

# video = cv2.VideoWriter
for image in images:
    frame = cv2.imread(directory + image)
    # height, width, layers = frame.shape
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(1.0/30.0)

cv2.destroyAllWindows()