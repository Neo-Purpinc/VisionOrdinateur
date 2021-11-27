import sys
import numpy as np
import cv2 as cv

# Create a function that add gaussian noise to an image with np.random.normal and a parameter sigma
def add_gaussian_noise(image):
    noise = cv.getTrackbarPos("Noise",window_title)
    gaussian = np.random.normal(0,np.abs(noise),image.shape[:2])
    noisy_image = np.zeros(image.shape,np.float32)
    if len(image.shape) == 2:
        noisy_image = image + gaussian
    else:
        noisy_image[:,:,0] = image[:,:,0] + gaussian
        noisy_image[:,:,1] = image[:,:,1] + gaussian
        noisy_image[:,:,2] = image[:,:,2] + gaussian
    cv.normalize(noisy_image,noisy_image,0,255,cv.NORM_MINMAX,dtype=-1)  
    noisy_image = noisy_image.astype(np.uint8)
    return noisy_image

def rotate_and_resize(image):
    angle = cv.getTrackbarPos("Angle",window_title)
    scale = float((cv.getTrackbarPos("Scale",window_title)+50)/100)
    width = int(cols*scale)
    height = int(rows*scale)
    M = cv.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv.warpAffine((image),M,(cols,rows))
    dst = cv.resize(dst,(width,height), interpolation = cv.INTER_NEAREST)
    return dst

def my_shi_tomasi(image):
    nb_points = cv.getTrackbarPos("Nb points",window_title)
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    print(nb_points)
    corners = cv.goodFeaturesToTrack(gray,nb_points,0.01,10)
    corners = np.int0(corners)
    for i in corners:
        x,y = i.ravel()
        cv.circle(image,(x,y),3,[0,255,0],-1)
    return image

def projection(image):
    if(nb_points_selectionnes==4):
        M = cv.getPerspectiveTransform(pts2,pts1)
        dst = cv.warpPerspective(image,M,(cols,rows))
        return dst
    else:
        return image

def display(x):
    #dst = add_gaussian_noise(img)
    dst = rotate_and_resize(img)
    dst = projection(dst)
    dst = my_shi_tomasi(dst)
    dst = np.uint8(dst)
    cv.imshow(window_title,dst)

def addPoint(event,x,y,flags,param):
    global nb_points_selectionnes
    if event == cv.EVENT_LBUTTONDOWN and nb_points_selectionnes<4:
        pts2[nb_points_selectionnes] = [x,y]
        nb_points_selectionnes += 1


if len(sys.argv) != 2:
    print("Usage: python3 exercice2.py <filename>")
    sys.exit(1)
img = cv.imread(sys.argv[1])
dst = None
rows, cols, channels = img.shape
window_title = "Shi-Tomasi"
nb_points_selectionnes = 0
pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
pts2 = np.float32([[0,0],[0,0],[0,0],[0,0]])

cv.namedWindow(window_title)
cv.createTrackbar("Angle",window_title,0,360,display)
cv.createTrackbar("Scale",window_title,50,100,display)
cv.createTrackbar("Noise",window_title,2,10,display)
cv.createTrackbar("Nb points",window_title,25,100,display)
cv.setMouseCallback(window_title,addPoint)
display("initialisation")
if cv.waitKey(0):
    cv.destroyAllWindows()