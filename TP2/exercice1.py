import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 3:
    sys.exit("Image path or n missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")
n = int(sys.argv[2])

kernel = np.ones((n,n))/(n**n)
dst = cv.filter2D(img,-1,kernel)

cv.imshow("Input image", img)
cv.imshow("Output image",dst)
cv.waitKey(0)