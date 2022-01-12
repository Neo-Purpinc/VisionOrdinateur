import cv2 as cv
import numpy as np
import sys
import argparse
import pafy

parser = argparse.ArgumentParser(description='This program use background subtraction implemented by Walid BEN SAID with frame differencing approach.')
parser.add_argument('--input', type=str, help='Path to a video.', default='../Videos/video1.avi')
parser.add_argument('--background',type=str,help="Path to the background image.", default='../Images/background.jpg')
args = parser.parse_args()

# url = "https://www.youtube.com/watch?v=EBhCrTPpdBI"
# video1 = pafy.new(url)
# best = video1.getbest(preftype="mp4")
# video = cv.VideoCapture(best.url)
video = cv.VideoCapture(args.input)
background = cv.imread(args.background,cv.IMREAD_COLOR)
kernel = np.ones((5,5),np.uint8)

re,current_frame = video.read()
previous_frame = current_frame
while(video.isOpened()):
    current_frame_gray = cv.cvtColor(current_frame,cv.COLOR_BGR2GRAY)
    previous_frame_gray = cv.cvtColor(previous_frame,cv.COLOR_BGR2GRAY)

    mask = cv.absdiff(current_frame_gray,previous_frame_gray)
    th, binary_mask = cv.threshold(mask,20,255,cv.THRESH_BINARY)
    binery_mask = cv.morphologyEx(cv.morphologyEx(binary_mask, cv.MORPH_OPEN, kernel,iterations=2),cv.MORPH_CLOSE,kernel,iterations=2)

    res = cv.resize(background,(current_frame.shape[1], current_frame.shape[0]))
    res[binary_mask==255] = current_frame[binary_mask==255]
    # cv.imshow('Mask',binary_mask)
    # cv.imshow('Frame',current_frame)
    cv.imshow('Res',res)
    if cv.waitKey(30) & 0xff == 27:
        break
    previous_frame = current_frame.copy()
    re,current_frame = video.read()
video.release()
cv.destroyAllWindows()