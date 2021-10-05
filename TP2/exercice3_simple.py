import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 2:
    sys.exit("Image path missing.")
img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")

#####################
## [ 0 , -1 , 0  ] ##
## [ -1 , 5 , -1 ] ##
## [ 0 , -1 , 0  ] ##
#####################
m3 = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
dst3 = cv.filter2D(img,-1,m3)

######################
## [ -1 , -1 , -1 ] ##
## [ -1 , 9 , -1  ] ##
## [ -1 , -1 , -1 ] ##
######################
m4 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
dst4 = cv.filter2D(img,-1,m4)

compareM3 = np.concatenate((img, dst3), axis=1)
compareM4 = np.concatenate((img, dst4), axis=1)
cv.imshow("Original & M3",compareM3)
cv.imshow("Original & M4",compareM4)

cv.waitKey(0)