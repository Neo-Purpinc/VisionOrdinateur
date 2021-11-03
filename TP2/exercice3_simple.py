
import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 2:
    sys.exit("Image path missing.")
img_8 = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
print(img_8.shape)
if img_8 is None:
    sys.exit("Could not read the image.")

#####################
## [ 0 , -1 , 0  ] ##
## [ -1 , 5 , -1 ] ##
## [ 0 , -1 , 0  ] ##
#####################
m3 = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
dst3 = cv.filter2D(img_8,cv.CV_16S,m3)
ret,thresh = cv.threshold(dst3,255,0,cv.THRESH_TRUNC)
ret,thresh2 = cv.threshold(thresh,0,0,cv.THRESH_TOZERO)
img3 = (thresh2).astype(np.uint8)

######################
## [ -1 , -1 , -1 ] ##
## [ -1 , 9 , -1  ] ##
## [ -1 , -1 , -1 ] ##
######################
m4 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
dst4 = cv.filter2D(img_8,cv.CV_16S,m4)
ret,thresh = cv.threshold(dst4,255,0,cv.THRESH_TRUNC)
ret,thresh2 = cv.threshold(thresh,0,0,cv.THRESH_TOZERO)
img4 = (thresh2).astype(np.uint8)

cv.imshow("Original",img_8)
cv.imshow("M3",img3)
cv.imshow("M4",img4)
cv.waitKey(0)