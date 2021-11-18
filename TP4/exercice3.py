import cv2 as cv
import sys
import numpy as np
i = 0
def addPoint(event,x,y,flags,param):
    global i
    if event == cv.EVENT_LBUTTONDOWN and i<3:
        pts2[i] = [x,y]
        i += 1
        if(i==3):
            M = cv.getAffineTransform(pts1,pts2)
            dst = cv.warpAffine(img,M,(cols,rows))
            cv.imshow("Transformation affine",dst)
            
if len(sys.argv) != 2:
    print("Usage: python3 exercice1.py <filename>")
    sys.exit(1)

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)

rows, cols, channels = img.shape
pts1 = np.float32([[0,0],[cols,0],[cols,rows]])
pts2 = np.float32([[0,0],[0,0],[0,0]])
cv.namedWindow("Transformation Affine")
cv.setMouseCallback('Transformation Affine',addPoint)
cv.imshow("Transformation Affine",img)

cv.waitKey(0)