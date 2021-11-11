import cv2 as cv
import sys
import numpy as np
import queue as q
import matplotlib.pyplot as plt

window_title = "TP3"
blurred,magnitude,mycanny,sigma,alpha,beta = None,None,None,None,None,None
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
    grad_d_copy =grad_d.copy()
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

def computeTresholds(grad_maxima, a, b):
    sorted_grad_maxima = np.sort(grad_maxima.copy(), axis=None)
    rang = round(a*len(sorted_grad_maxima))
    if a == 1:
        rang -= 1
    thigh = sorted_grad_maxima[rang]
    tlow = b*thigh
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

def mycannyfunc(image,s,a,b):
    blur = gaussianFiltering(image,s)
    sobelx64f = computeGx(blur)
    sobely64f = computeGy(blur)
    magnitude_64 = computeMagnitude(sobelx64f,sobely64f)
    direction_64 = computeDirection(sobelx64f,sobely64f)
    gmax_64 = removeNonMaxima(magnitude_64,direction_64)
    tHigh, tLow = computeTresholds(gmax_64,a,b)
    mycanny_64 = hysteresisThresholding(gmax_64,tLow,tHigh)
    magn = np.uint8(magnitude_64)
    mycanny = np.uint8(mycanny_64)
    canny = cv.Canny(blur,tHigh,tLow,L2gradient=True)
    writeOutput(s,a,b,tHigh,tLow)
    return blur,magn,mycanny,canny

def writeOutput(s,a,b,tHigh,tLow):
    print("Avec les paramètres sigma = "+str(s)+", alpha = "+str(a)+
    " et beta = "+str(b)+",\ntHigh = "+str(tHigh)+"\ttLow = "+str(tLow)+"\n")

def writeImage(blur,magn,mycanny,s,a,b):
    cv.imwrite("Blurred_"+str(s)+".jpg",blur)
    cv.imwrite("Magnitude_"+str(s)+"_"+str(a)+"_"+str(b)+".jpg",magn)
    cv.imwrite("MyCanny_"+str(s)+"_"+str(a)+"_"+str(b)+".jpg",mycanny)

def display(x):
    sigma = float(cv.getTrackbarPos("Sigma",window_title))
    alpha = float(cv.getTrackbarPos("Alpha",window_title))/20.
    beta = float(cv.getTrackbarPos("Beta",window_title))/20.
    blurred,magnitude,mycanny,canny = mycannyfunc(img,sigma,alpha,beta)
    cv.imshow(window_title,np.concatenate([mycanny,canny],axis=1))
    if ((x=="initialisation" and len(sys.argv) == 5) or x=="pressS"):
        writeImage(blurred,magnitude,mycanny,sigma,alpha,beta)
    
if len(sys.argv) == 2:
    sigma_user = 2
    alpha_user = 19
    beta_user = 16
elif len(sys.argv) == 5:
    sigma_user = int(sys.argv[2])
    alpha_user = int(float(sys.argv[3])*20)
    beta_user = int(float(sys.argv[4])*20)
else:
    sys.exit("Please, add at least image path.\n"+
            "You can also give sigma for the GaussianBlur in addition to alpha and beta for the thresholds.")
img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_GRAYSCALE)
cv.namedWindow(window_title)
cv.createTrackbar("Sigma",window_title,sigma_user,20,display)
cv.createTrackbar("Alpha",window_title,alpha_user,20,display)
cv.createTrackbar("Beta",window_title,beta_user,20,display)
display("initialisation")
while True:
    x = cv.waitKey(1) & 0xFF
    if(x == ord('s') or x == ord('S')):
        display("pressS")
        print("Vos images ont bien été sauvegardées.\n")
    elif x == 27 or x == ord('q') or x == ord('Q'):
        break
    