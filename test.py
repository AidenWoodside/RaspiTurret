#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test.py
#  
#  Copyright 2024  <woods@turret>



def main(args):
    picam = Picamera2()
    picam.preview_configuration.main.size=(1280,720)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()
        
    while True:
        frame = picam.capture_array()
        frame = cv2.flip(frame, 0)
        cv2.namedWindow("Camera", 16)
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1)==ord('q'):
            break
    cv2.destroyAllWindows()
    
    return 0

if __name__ == '__main__':
    import sys
    import cv2
    from picamera2 import Picamera2
    import time
    sys.exit(main(sys.argv))
