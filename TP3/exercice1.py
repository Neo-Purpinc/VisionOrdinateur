import cv2 as cv
import sys
import numpy as np
import math as mt
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
    return np.sqrt(gx*gx+gy*gy)

def computeDirection(gx,gy):
    #Entre 0 et 2 PI
    return np.arctan2(gy,gx)   

def removeNonMaxima(grad_m, grad_d):
    M, N = grad_m.shape[0:2]
    gmax = grad_m.copy()
    # On passe de l'intervalle [ 0 , 2pi ] à [ -pi , pi ]
    grad_d_moins_pi_pi = np.array(grad_d) - mt.pi
    for i in range(1,M-1):
        for j in range(1,N-1):
            # On ramène dans l'intervalle [ -pi/8 , 7pi/8 [
            if(grad_d_moins_pi_pi[i,j] < -mt.pi/8):
                grad_d_moins_pi_pi[i,j] += mt.pi
            elif(grad_d_moins_pi_pi[i,j] >= 7*mt.pi/8):
                grad_d_moins_pi_pi[i,j] -= mt.pi
            # Horizontal
            if(-(mt.pi/8)<= grad_d_moins_pi_pi[i,j] < mt.pi/8):
                a = grad_m[i,j-1]
                b = grad_m[i,j+1]
            # Diagonal 45
            elif(mt.pi/8 <= grad_d_moins_pi_pi[i,j] < 3*mt.pi/8):
                a = grad_m[i-1,j-1]
                b = grad_m[i+1,j+1]
            # Vertical 90
            elif(3*mt.pi/8 <= grad_d_moins_pi_pi[i,j] < 5*mt.pi/8):
                a = grad_m[i-1,j]
                b = grad_m[i+1,j]
            #Diagonal 135
            elif(5*mt.pi/8 <= grad_d_moins_pi_pi[i,j] < 7*mt.pi/8):
                a = grad_m[i-1,j+1]
                b = grad_m[i+1,j-1]
            # Non-max Suppression
            if(not((grad_m[i,j] >= a) and (grad_m[i,j] >= b))):
                gmax[i,j] = 0
    return gmax

def computeTresholds(grad_maxima, alpha, beta):
    sorted_grad_maxima = np.sort(grad_maxima.copy())
    n = len(sorted_grad_maxima)
    print(n)
    thigh = sorted_grad_maxima[round(alpha*n)]
    tlow = beta*thigh
    return thigh, tlow

def test():
    img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_GRAYSCALE)

    blurred = gaussianFiltering(img,1)

    sobelx64f = computeGx(blurred)
    abs_sobelx64f = np.absolute(sobelx64f)
    sobelx_8u = np.uint8(abs_sobelx64f)

    sobely64f = computeGy(blurred)
    abs_sobely64f = np.absolute(sobely64f)
    sobely_8u = np.uint8(abs_sobely64f)

    magnitude_64 = computeMagnitude(sobelx64f,sobely64f)
    magnitude = np.uint8(magnitude_64)

    direction_64 = computeDirection(sobelx64f,sobely64f)
    direction = np.uint8(direction_64)

    gmax_64 = removeNonMaxima(magnitude,direction)
    gmax = np.uint8(gmax_64)

    computeTresholds(gmax_64,1,2)
    cv.imshow("Original",img)
    cv.imshow("Blurred",blurred)
    cv.imshow("Sobel X",sobelx_8u)
    cv.imshow("Sobel Y",sobely_8u)
    cv.imshow("Magnitude",magnitude)
    cv.imshow("Direction",direction)
    cv.imshow("Non-Maxima",gmax)
    cv.waitKey(0)

test()

