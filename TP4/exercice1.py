import cv2 as cv
import sys
import numpy as np
# Verify that the user has provided a filename, x and y
if len(sys.argv) != 4:
    print("Usage: python3 exercice1.py <filename> <x> <y>")
    sys.exit(1)

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
x = sys.argv[2]
y = sys.argv[3]
rows,cols = img.shape[0:2]
M = np.float32([[1,0,x],[0,1,y]])
dst = cv.warpAffine(img,M,(cols,rows))
res = np.concatenate((img,dst),axis=1)
cv.imshow('Résultat',res)
cv.waitKey(0)
