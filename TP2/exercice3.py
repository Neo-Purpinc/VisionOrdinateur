import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 2:
    sys.exit("Image path missing.")
img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")

m3 = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
dst3 = cv.normalize(img, cv.filter2D(img,-1,m3), 0, 255, cv.NORM_MINMAX)

m4 = np.array([[-1,-1,-1],[-1,9,-1],[-1,-1,-1]])
dst4 = cv.normalize(img, cv.filter2D(img,-1,m4), 0, 255, cv.NORM_MINMAX)

cv.namedWindow('Input image')
cv.imshow("Input image",img)
cv.imshow("Output image M3",dst3)
cv.imshow("Output image M4",dst4)
cv.waitKey(0)