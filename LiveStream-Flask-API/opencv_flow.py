import numpy as np
import cv2
import argparse

cap = cv2.VideoCapture(1)
while(1):
    ret,frame = cap.read()
    cv2.imshow('frame',frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # Now update the previous frame and previous points

cap.release()
cv2.destroyAllWindows()