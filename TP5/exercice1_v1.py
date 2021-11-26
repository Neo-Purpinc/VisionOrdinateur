import cv2 as cv
import sys
import numpy as np

def isInImage(image,x,y):
    M,N = image.shape
    res = True
    if x >= M or x < 0 or y < 0 or y >= N:
        res = False
    return res

def gaussianFiltering(f,s):
    n = int(3*s)
    if(n%2 == 0):
        n = n+1
    return cv.GaussianBlur(f,(n,n),s)

def removeNonMaxima(f):
    #f = gaussianFiltering(img,s)
    gx = cv.Sobel(f,cv.CV_64F,1,0)
    gy = cv.Sobel(f,cv.CV_64F,0,1)
    grad_m = np.sqrt(gx**2+gy**2)
    grad_d = np.arctan2(gy,gx)   
    M, N = grad_m.shape
    gmax = f.copy()
    grad_d_copy = grad_d.copy()
    for i in range(M):
        for j in range(N):
            a = None
            # On ramène dans l'intervalle [ -pi/8 , 7pi/8 [
            if(grad_d_copy[i,j] < -np.pi/8):
                grad_d_copy[i,j] += np.pi
            elif(grad_d_copy[i,j] >= 7*np.pi/8):
                grad_d_copy[i,j] -= np.pi
            # Horizontal
            if(-np.pi/8 <= grad_d_copy[i,j] < np.pi/8) and isInImage(grad_m,i,j-1) and isInImage(grad_m,i,j+1):
                a = grad_m[i,j-1]
                b = grad_m[i,j+1]
            # Diagonal 45
            elif(np.pi/8 <= grad_d_copy[i,j] < 3*np.pi/8) and isInImage(grad_m,i-1,j-1) and isInImage(grad_m,i+1,j+1):
                a = grad_m[i-1,j-1]
                b = grad_m[i+1,j+1]
            # Vertical 90
            elif(3*np.pi/8 <= grad_d_copy[i,j] < 5*np.pi/8) and isInImage(grad_m,i-1,j) and isInImage(grad_m,i+1,j):
                a = grad_m[i-1,j]
                b = grad_m[i+1,j]
            #Diagonal 135
            elif(5*np.pi/8 <= grad_d_copy[i,j] < 7*np.pi/8) and isInImage(grad_m,i-1,j+1) and isInImage(grad_m,i+1,j-1):
                a = grad_m[i-1,j+1]
                b = grad_m[i+1,j-1]
            # Non-max Suppression
            if a is not None:
                if(a > grad_m[i,j] or b > grad_m[i,j]):
                    gmax[i,j] = 0
    return gmax

def harrisFunc(img):
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv.cornerHarris(gray,3,3,0.01)
    i_dlt = cv.dilate(dst,None)
    img[dst>0.01*dst.max()]=[0,0,255]
    return img

def display(x):
    angle = cv.getTrackbarPos("Angle",window_title)
    scale = float((cv.getTrackbarPos("Scale",window_title)+50)/100)
    width = int(cols*scale)
    height = int(rows*scale)
    M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv.warpAffine(image,M,(cols,rows))
    dst = cv.resize(dst,(width,height), interpolation = cv.INTER_NEAREST)
    harris = harrisFunc(dst)
    cv.imshow(window_title,harris)

if len(sys.argv) != 2:
    print("Usage: python3 exercice1.py <filename>")
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