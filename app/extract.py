import cv2 as cv
import numpy as np

def color_segmentation(image, lower, upper):
    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.inRange(hsv, lower, upper)
    
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    
    return mask