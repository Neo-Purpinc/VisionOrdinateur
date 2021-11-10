import cv2 as cv
import sys
import numpy as np
import queue as q
import matplotlib.pyplot as plt

window_title = "TP3"

def isInImage(image,x,y):
    M,N = image.shape
    res = True
    if x >= M or x < 0 or y < 0 or y >= N:
        res = False
    return res

def gaussianFiltering(f,sigma):
    n = int(3*sigma)
    if(n%2 == 0):
        n = n+1
    return cv.GaussianBlur(f,(n,n),sigma)

def computeGx(f):
    return cv.Sobel(f,cv.CV_64F,1,0)

def computeGy(f):
    return cv.Sobel(f,cv.CV_64F,0,1)

def computeMagnitude(gx,gy):
    return np.sqrt(gx**2+gy**2)

def computeDirection(gx,gy):
    #Entre 0 et 2 PI
    return np.arctan2(gy,gx)   

def removeNonMaxima(grad_m, grad_d):
    M, N = grad_m.shape
    gmax = grad_m.copy()
    # On passe de l'intervalle [ 0 , 2pi ] à [ -pi , pi ]
    grad_d_moins_pi_pi =grad_d.copy()
    # map(lambda x: x if x <= np.pi else x - 2*np.pi, grad_d_moins_pi_pi)
    for i in range(M):
        for j in range(N):
            a = None
            # On ramène dans l'intervalle [ -pi/8 , 7pi/8 [
            if(grad_d_moins_pi_pi[i,j] < -np.pi/8):
                grad_d_moins_pi_pi[i,j] += np.pi
            elif(grad_d_moins_pi_pi[i,j] >= 7*np.pi/8):
                grad_d_moins_pi_pi[i,j] -= np.pi
            # Horizontal
            if(-np.pi/8 <= grad_d_moins_pi_pi[i,j] < np.pi/8) and isInImage(grad_m,i,j-1) and isInImage(grad_m,i,j+1):
                a = grad_m[i,j-1]
                b = grad_m[i,j+1]
            # Diagonal 45
            elif(np.pi/8 <= grad_d_moins_pi_pi[i,j] < 3*np.pi/8) and isInImage(grad_m,i-1,j-1) and isInImage(grad_m,i+1,j+1):
                a = grad_m[i-1,j-1]
                b = grad_m[i+1,j+1]
            # Vertical 90
            elif(3*np.pi/8 <= grad_d_moins_pi_pi[i,j] < 5*np.pi/8) and isInImage(grad_m,i-1,j) and isInImage(grad_m,i+1,j):
                a = grad_m[i-1,j]
                b = grad_m[i+1,j]
            #Diagonal 135
            elif(5*np.pi/8 <= grad_d_moins_pi_pi[i,j] < 7*np.pi/8) and isInImage(grad_m,i-1,j+1) and isInImage(grad_m,i+1,j-1):
                a = grad_m[i-1,j+1]
                b = grad_m[i+1,j-1]
            # Non-max Suppression
            if a is not None:
                if(a > grad_m[i,j] or b > grad_m[i,j]):
                    gmax[i,j] = 0
    return gmax

def computeTresholds(grad_maxima, alpha, beta):
    sorted_grad_maxima = np.sort(grad_maxima.copy(), axis=None)
    n = len(sorted_grad_maxima)
    rang = round(alpha*n)
    if alpha == 1:
        rang -= 1
    thigh = sorted_grad_maxima[rang]
    tlow = beta*thigh
    return thigh, tlow

def hysteresisThresholding(grad_maxima, tLow, tHigh):   
    fifo = q.Queue()
    canny = np.zeros_like(grad_maxima)
    M,N = grad_maxima.shape
    for i in range(M):
        for j in range(N):
            if grad_maxima[i,j] >= tHigh:
                fifo.put((i,j))
                canny[i,j] = 255
    while not fifo.empty():
        (a,b) = fifo.get()
        voisins8 = [(a-1,b-1),(a-1,b),(a-1,b+1),(a+1,b-1),(a+1,b),(a+1,b+1),(a,b-1),(a,b+1)]
        for (c,d) in voisins8:
            if isInImage(grad_maxima,c,d) and grad_maxima[c,d] >= tLow and canny[c,d]==0:
                canny[c,d] = 255
                fifo.put((c,d))
    return canny

def mycannyfunc(image,sigma,alpha,beta):
    blurred = gaussianFiltering(image,sigma)
    sobelx64f = computeGx(blurred)
    sobely64f = computeGy(blurred)
    magnitude_64 = computeMagnitude(sobelx64f,sobely64f)
    magnitude = np.uint8(magnitude_64)
    direction_64 = computeDirection(sobelx64f,sobely64f)
    gmax_64 = removeNonMaxima(magnitude_64,direction_64)
    tHigh, tLow = computeTresholds(gmax_64,alpha,beta)
    print("tHigh = "+str(tHigh)+"\ttLow = "+str(tLow))
    mycanny_64 = hysteresisThresholding(gmax_64,tLow,tHigh)
    mycanny = np.uint8(mycanny_64)
    ecrireImage(blurred,magnitude,mycanny)
    return mycanny,blurred, tHigh, tLow

def ecrireImage(blurred,magnitude,mycanny):
    cv.imwrite("Blurred.jpg",blurred)
    cv.imwrite("Magnitude.jpg",magnitude)
    cv.imwrite("MyCanny.jpg",mycanny)

def display(x):
    sigma = float(cv.getTrackbarPos("Sigma",window_title))
    alpha = float(cv.getTrackbarPos("Alpha",window_title))/20.
    beta = float(cv.getTrackbarPos("Beta",window_title))/20.
    mycannyres, blur, thigh, tlow = mycannyfunc(img,sigma,alpha,beta)
    cv.imshow(window_title,np.concatenate([mycannyres, cv.Canny(blur,thigh,tlow,L2gradient=True)],axis=1))

cv.namedWindow(window_title)
img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_GRAYSCALE)
cv.createTrackbar("Sigma",window_title,2,20,display)
cv.createTrackbar("Alpha",window_title,19,20,display)
cv.createTrackbar("Beta",window_title,16,20,display)
display("initialisation")
cv.waitKey(0)