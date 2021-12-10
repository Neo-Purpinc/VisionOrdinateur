import cv2 as cv
import sys
import numpy as np

def harrisFunc(img,n):
    gray = np.float32(cv.cvtColor(img,cv.COLOR_BGR2GRAY))
    dst = cv.cornerHarris(gray,3,3,0.01)
    i_dlt = cv.dilate(dst,None)
    tmp = np.float32(np.zeros(gray.shape))
    tmp[np.logical_and(dst>0.01*dst.max(),dst==i_dlt)] = 255
    tmp = cv.dilate(tmp1,None)
    img[tmp==255]=[0,0,255]
    
    xmin = x-n/2
    xmax = x+n/2
    w = img[xmin:xmax,ymin:ymax].flatten

    return np.uint8(img1)

if len(sys.argv) != 3:
    print("Usage: python3 Harris.py <filename1> <filename2> <n>")
    sys.exit(1)
image1 = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
image2 = cv.imread(sys.argv[2],cv.IMREAD_COLOR)
n = sys.argv[3]
window_title = "Harris"
cv.namedWindow(window_title)

final1,final2 = harrisFunc(image1,n),harrisFunc(image2,n)
dst = np.concatenate((final1,final2),axis=1)
cv.imshow(window_title,dst)
if cv.waitKey(0) & 0xff == 27:
    cv.destroyAllWindows()