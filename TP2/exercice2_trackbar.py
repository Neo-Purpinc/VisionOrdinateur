import cv2 as cv
import sys
import numpy as np

window_title = "Original & Smoothed"
def display(x):
    s = float(cv.getTrackbarPos("Sigma",window_title))
    n = int(3*s)
    if(n%2 == 0):
        n = n+1
    dst = cv.GaussianBlur(img,(n,n),s)
    final = np.concatenate((img,dst),axis=1)
    cv.imshow(window_title,final)

if len(sys.argv) != 2:
    sys.exit("Image path missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")

cv.namedWindow(window_title)
cv.createTrackbar("Sigma",window_title,0,20,display)
display("initialisation")
cv.waitKey(0)