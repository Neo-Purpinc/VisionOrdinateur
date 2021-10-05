import cv2 as cv
import sys
import numpy as np

window_title = "Original - Smoothed - M3 smoothed - M4 smoothed"
def display(x):
    s = float(cv.getTrackbarPos("Sigma",window_title))
    n = int(3*s)
    if(n%2 == 0):
        n = n+1
    dst = cv.GaussianBlur(img,(n,n),s)
    dst3 = cv.filter2D(dst,-1,m3)
    dst4 = cv.filter2D(dst,-1,m4)
    tmp1 = np.concatenate((img,dst),axis=1)
    tmp2 = np.concatenate((dst3,dst4),axis=1)
    final = np.concatenate((tmp1,tmp2),axis=1)
    cv.imshow(window_title,final)

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
######################
## [ -1 , -1 , -1 ] ##
## [ -1 , 9 , -1  ] ##
## [ -1 , -1 , -1 ] ##
######################
m4 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
cv.namedWindow(window_title)
cv.createTrackbar("Sigma",window_title,0,20,display)
display("initialisation")
cv.waitKey(0)