import cv2 as cv
import numpy as np
import sys
import argparse

parser = argparse.ArgumentParser(description='This program use background subtraction methods provided by \
                                              OpenCV.')
parser.add_argument('--input', type=str, help='Path to a video.', default='../Videos/video1.avi')
parser.add_argument('--background',type=str,help="Path to the output image file.", default='../Images/times_square.jpg')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

video = cv.VideoCapture(args.input)
background = cv.imread(args.output,cv.IMREAD_COLOR)
if args.algo == 'MOG2':
    bgSub = cv.createBackgroundSubtractorMOG2()
else:
    bgSub = cv.createBackgroundSubtractorKNN()

kernel = np.ones((5,5),np.uint8)
while(video.isOpened()):
    ret,frame_o = video.read()
    if ret is True:
        frame = cv.resize(frame_o,(800,500))
        frame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        mask = cv.morphologyEx(cv.morphologyEx(bgSub.apply(frame), cv.MORPH_OPEN, kernel,iterations=2),cv.MORPH_CLOSE,kernel,iterations=2)
        res= cv.resize(background,(frame.shape[1], frame.shape[0]))
        res[mask==255] = frame[mask==255]
        # cv.imshow('Mask',mask)
        # cv.imshow('Frame',frame)
        cv.imshow('Res',res)
        if cv.waitKey(30) & 0xff == 27:
            break
    else:
        break
video.release()
cv.destroyAllWindows()