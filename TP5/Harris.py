import cv2 as cv
import sys
import numpy as np

def harrisFunc(img):
    gray = np.float32(cv.cvtColor(img,cv.COLOR_BGR2GRAY))
    dst = cv.cornerHarris(gray,3,3,0.01)
    i_dlt = cv.dilate(dst,None)

    tmp = np.float32(np.zeros(gray.shape))
    tmp[np.logical_and(dst>0.01*dst.max(),dst==i_dlt)] = 255
    tmp = cv.dilate(tmp,None)
    
    img[tmp==255]=[0,0,255]
    return img

def display(x):
    angle = cv.getTrackbarPos("Angle",window_title)
    scale = float((cv.getTrackbarPos("Scale",window_title)+50)/100)
    width = int(cols*scale)
    height = int(rows*scale)
    M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv.warpAffine(image,M,(cols,rows))
    dst = cv.resize(dst,(width,height), interpolation = cv.INTER_NEAREST)
    harris = np.uint8(harrisFunc(dst))
    cv.imshow(window_title,harris)

if len(sys.argv) != 2:
    print("Usage: python3 Harris.py <filename>")
    sys.exit(1)
image = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
rows, cols, channels = image.shape
window_title = "Harris"

cv.namedWindow(window_title)
cv.createTrackbar("Angle",window_title,0,360,display)
cv.createTrackbar("Scale",window_title,50,100,display)
display("initialisation")
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()