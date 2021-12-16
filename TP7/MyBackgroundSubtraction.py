import cv2 as cv
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage: python3 MyBackgroundSubtraction.py <videoPath> <BackgroundImagePath>")
    sys.exit(1)
video = cv.VideoCapture(sys.argv[1])
background = cv.imread(sys.argv[2],cv.IMREAD_COLOR)
bgSub = cv.createBackgroundSubtractorMOG2()
kernel = np.ones((5,5),np.uint8)