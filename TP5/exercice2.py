import sys
import numpy as np
import cv2 as cv

if len(sys.argv) != 2:
    print("Usage: python3 exercice2.py <filename>")
    sys.exit(1)

img = cv.imread(sys.argv[1])
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
corners = cv.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)

cv.imshow('dst',img)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()