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

cv.imshow("Input image", img)
cv.imshow("Output image",dst)
cv.waitKey(0)