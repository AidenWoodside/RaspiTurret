#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test.py
#  
#  Copyright 2024  <woods@turret>

def FindContours(img):
    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
    
    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
    
    # Canny Edge Detection
    return cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection

def FindGreenBall(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #set the lower and upper bounds for the green hue
    lower_green = np.array([50,75,50])
    upper_green = np.array([100,255,255])

    #create a mask for green colour using inRange function
    mask = cv2.inRange(hsv, lower_green, upper_green)

    #perform bitwise and on the original image arrays using the mask
    res = cv2.bitwise_and(img, img, mask=mask)
    ret,thresh = cv2.threshold(mask,127,255,0)

    contours, hierarchy = cv2.findContours(thresh.astype(np.uint8), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    

    if len(contours) != 0:
        c = max(contours, default = 0, key = cv2.contourArea)
        if cv2.contourArea(c) > 20:
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            else:
                cX, cY = 0, 0
            cv2.drawContours(img, c, -1, 255, 3)
            cv2.circle(img, (cX, cY), 7, (255, 255, 255), -1)



    cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
    return img


def main(args):
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    #declare reference to pi camera 
    picam = Picamera2()
    picam.preview_configuration.main.size=(640,480)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
        
    while True:
        #grab image from the camera
        frame = picam.capture_array()

        #flip image so that it is the right direction
        frame = cv2.flip(frame, 0)
        
        #run the image transformations 
        #output = FindContours(frame)
        output = FindGreenBall(frame)

        #display the output image
        cv2.imshow("Camera", output)
        if cv2.waitKey(1)==ord('q'):
            break
    cv2.destroyAllWindows()
    
    return 0


if __name__ == '__main__':
    import sys
    import cv2
    from picamera2 import Picamera2
    import numpy as np
    sys.exit(main(sys.argv))
