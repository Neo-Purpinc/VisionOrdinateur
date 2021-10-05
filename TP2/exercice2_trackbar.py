import cv2 as cv
import sys
import numpy as np

def display(x):
    s = float(cv.getTrackbarPos("sigma","Input image"))
    n = int(3*s)
    if(n%2 == 0):
        n = n+1
    dst = cv.GaussianBlur(img,(n,n),s)
    cv.imshow("Output image",dst)

if len(sys.argv) != 2:
    sys.exit("Image path missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")

cv.namedWindow('Input image')
cv.imshow("Input image", img)
cv.createTrackbar("sigma","Input image",0,20,display)
display("initialisation")
cv.waitKey(0)