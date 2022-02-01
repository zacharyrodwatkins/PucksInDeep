# import the opencv library
import cv2
  
  
# define a video capture object
vid = cv2.VideoCapture(0)
  
while(True):
      
    # Capture the video frame
    ret, frame = vid.read()
    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_min = (0, int(0.6*255), int(0.20*255))
    hsv_max = (8, int(0.98*255), int(0.80*255))
    low_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
    hsv_min = (175, int(0.6*255), int(0.40*255))
    hsv_max = (180, int(0.98*255), int(0.80*255))
    high_hue_bin_img = cv2.inRange(hsv_img, hsv_min, hsv_max)
    bin_img = low_hue_bin_img + high_hue_bin_img
    binvert = cv2.bitwise_not(bin_img)
    M = cv2.moments(bin_img)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    


    cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
    # Display the resulting frames
    cv2.imshow('bin', frame)

    cv2.imshow('inv', binvert)
    # cv2.imshow('low', low_hue_bin_img)
    # cv2.imshow('high', high_hue_bin_img)
    # cv2.imshow('frame', frame)  
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()