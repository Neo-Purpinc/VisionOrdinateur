import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 3:
    sys.exit("Image path or sigma missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")
s = float(sys.argv[2])
n = int(3*s)

if(n%2 == 0):
    n = n+1

dst = cv.GaussianBlur(img,(n,n),s)

ret = np.concatenate((img, dst), axis=1)
cv.imshow("Original & Smoothed", ret)
cv.waitKey(0)