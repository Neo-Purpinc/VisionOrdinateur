import cv2 as cv
import numpy as np
import sys
import argparse
import pafy

parser = argparse.ArgumentParser(description='This program use background subtraction implemented by Walid BEN SAID with Gaussian average approach.')
parser.add_argument('--input', type=str, help='Path to a video.', default='../Videos/video1.mp4')
parser.add_argument('--background',type=str,help="Path to the background image.", default='../Images/background.jpg')
args = parser.parse_args()

# url = "https://www.youtube.com/watch?v=EBhCrTPpdBI"
# video1 = pafy.new(url)
# best = video1.getbest(preftype="mp4")
# video = cv.VideoCapture(best.url)
video = cv.VideoCapture(args.input)
background = cv.imread(args.background,cv.IMREAD_COLOR)
kernel = np.ones((3,3),np.uint8)

re,current_frame = video.read()
moyenne = cv.cvtColor(current_frame,cv.COLOR_BGR2GRAY)
(col,row) = moyenne.shape
variance = np.ones((col,row),np.uint8)
variance[:col,:row] = 100

p = 0.01
k = 2.5
#From https://en.wikipedia.org/wiki/Foreground_detectionhttps://en.wikipedia.org/wiki/Foreground_detection
while(video.isOpened()):
    current_frame_gray = cv.cvtColor(current_frame,cv.COLOR_BGR2GRAY)
    current_frame_gray = cv.GaussianBlur(current_frame_gray,(3,3),2)
    newMoyenne = p*current_frame_gray + (1-p)*moyenne 
    newMoyenne = newMoyenne.astype(np.uint8)
    newVariance = (p)*(cv.subtract(current_frame_gray,moyenne,dtype=-1)**2)+(1-p)*variance
    value = cv.absdiff(current_frame_gray,moyenne)/ np.sqrt(variance)
    moyenne = np.where(value<k,newMoyenne,moyenne)
    variance = np.where(value<k,newVariance,variance)
    b = np.uint8([0])
    mask =  cv.morphologyEx(np.where(value>k,current_frame_gray,b), cv.MORPH_OPEN, kernel)
    th, binary_mask = cv.threshold(mask,20,255,cv.THRESH_BINARY)
    res = cv.resize(background,((current_frame.shape[1], current_frame.shape[0])))
    res[binary_mask==255] = current_frame[binary_mask==255]
    # cv.imshow('Foreground',binary_mask)
    cv.imshow('Res',res)
    if cv.waitKey(30) & 0xff == 27:
        break
    previous_frame = current_frame.copy()
    re,current_frame = video.read()

video.release()

cv.destroyAllWindows()