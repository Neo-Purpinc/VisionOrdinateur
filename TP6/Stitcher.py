import numpy as np
import cv2 as cv
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python3 Stitcher.py <directory>")
    sys.exit(1)
directory = sys.argv[1]
files = []
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    files.append(f)
files.sort()
imgs = []
for f in files:
    imgs.append(cv.imread(f,cv.IMREAD_COLOR))

stitcher = cv.Stitcher.create(cv.Stitcher_PANORAMA)
status,pano = stitcher.stitch(imgs)
res = cv.resize(pano,(pano.shape[1]//2,pano.shape[0]//2))
cv.imshow("Panorama",res)

cv.waitKey(0)