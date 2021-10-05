import cv2 as cv
import sys
import numpy as np

if len(sys.argv) != 3:
    sys.exit("Image path or n missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")
n = int(sys.argv[2])

dst = cv.blur(img,(n,n))


ret = np.concatenate((img, dst), axis=1)
cv.imshow("Original & Blurred", ret)
cv.waitKey(0)