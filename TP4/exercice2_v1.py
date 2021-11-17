import cv2 as cv
import sys
import numpy as np

def display(x):
    angle = cv.getTrackbarPos("Angle","Rotation")
    M = cv.getRotationMatrix2D((centreX,centreY),angle,1)
    dst = cv.warpAffine(img,M,(cols,rows))
    res = np.concatenate((img,dst),axis=1)
    cv.imshow("Rotation",res)
    
if len(sys.argv) != 5:
    print("Usage: python3 exercice1.py <filename> <angle> <centerX> <centerY>")
    sys.exit(1)

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
angle =  int(sys.argv[2])
centreX = float(sys.argv[3])
centreY = float(sys.argv[4])
rows, cols, channels = img.shape

cv.namedWindow("Rotation")
cv.createTrackbar("Angle","Rotation",angle,360,display)
display("Initialisation")
cv.waitKey(0)