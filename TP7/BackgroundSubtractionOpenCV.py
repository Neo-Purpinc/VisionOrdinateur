import cv2 as cv
import numpy as np
import sys
import argparse
# import pafy

parser = argparse.ArgumentParser(description='This program use background subtraction methods provided by OpenCV.')
parser.add_argument('--input', type=str, help='Path to a video.', default='../Videos/video2.mp4')
parser.add_argument('--background',type=str,help="Path to the output image file.", default='../Images/background.jpg')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')
args = parser.parse_args()

# url = "https://www.youtube.com/watch?v=EBhCrTPpdBI"
# video1 = pafy.new(url)
# best = video1.getbest(preftype="mp4")
# video = cv.VideoCapture(best.url)

video = cv.VideoCapture(args.input)
background = cv.imread(args.background,cv.IMREAD_COLOR)
if args.algo == 'MOG2':
    bgSub = cv.createBackgroundSubtractorMOG2(detectShadows=False)
else:
    bgSub = cv.createBackgroundSubtractorKNN(detectShadows=False)

kernel = np.ones((5,5),np.uint8)
while(video.isOpened()):
    ret,frame = video.read()
    if ret is True:
        # frame = cv.resize(frame_o,(800,500))
        mask = cv.morphologyEx(cv.morphologyEx(bgSub.apply(frame), cv.MORPH_OPEN, kernel,iterations=2),cv.MORPH_CLOSE,kernel,iterations=2)
        th, mask = cv.threshold(mask,20,255,cv.THRESH_BINARY)
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