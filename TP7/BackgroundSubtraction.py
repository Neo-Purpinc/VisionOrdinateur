import cv2 as cv
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage: python3 BackgroundSubtraction.py <videoPath> <BackgroundImagePath>")
    sys.exit(1)
video = cv.VideoCapture(sys.argv[1])
background = cv.imread(sys.argv[2],cv.IMREAD_COLOR)
bgSub = cv.createBackgroundSubtractorMOG2()
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(10,10))
while(video.isOpened()):
    ret,frame_o = video.read()
    if ret is True:
        frame = cv.resize(frame_o,(800,500))
        mask = cv.morphologyEx(cv.morphologyEx(bgSub.apply(frame), cv.MORPH_OPEN, kernel),cv.MORPH_CLOSE,kernel)
        res= cv.resize(background,(frame.shape[1], frame.shape[0]))
        res[mask==255] = frame[mask==255]
        cv.imshow('Mask',mask)
        cv.imshow('Frame',frame)
        cv.imshow('Res',res)
        if cv.waitKey(30) & 0xff == 27:
            break
    else:
        break
video.release()
cv.destroyAllWindows()