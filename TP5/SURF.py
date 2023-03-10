import sys
import numpy as np
import cv2 as cv

if len(sys.argv) != 2:
    print("Usage: python3 SURF.py <filename>")
    sys.exit(1)

img = cv.imread(sys.argv[1],cv.IMREAD_COLOR)
current = img
dst = None
rows, cols = img.shape[:2]
window_title = "SURF"
nb_points_selectionnes = 0
pts1 = np.float32([[0,0],[cols,0],[cols,rows],[0,rows]])
pts2 = np.float32([[0,0],[0,0],[0,0],[0,0]])

def add_gaussian_noise(image):
    noise = cv.getTrackbarPos("Noise",window_title)
    gaussian = np.random.normal(0,np.abs(noise),image.shape[:2]).astype(np.float32)
    noisy_image = np.zeros(image.shape,np.float32)
    image = image.astype(np.float32)
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
    width = int(image.shape[1]*scale)
    height = int(image.shape[0]*scale)
    M = cv.getRotationMatrix2D((image.shape[1]/2,image.shape[0]/2),angle,1)
    dst = cv.warpAffine((image),M,(image.shape[1],image.shape[0]))
    dst = cv.resize(dst,(width,height), interpolation = cv.INTER_NEAREST)
    return dst

def my_surf(image):
    nb_pts = cv.getTrackbarPos("Nb points",window_title)
    surf = cv.SURF_create(400)
    gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    kp = surf.detect(gray,None)
    j=0
    for i in cv.KeyPoint_convert(kp):
        j+=1
        x,y = i.ravel()
        cv.circle(image,(int(x),int(y)),3,[0,255,0],-1)
        if nb_pts!=0 and j>=nb_pts:
            break
    return image

def projection(image):
    if(nb_points_selectionnes==4):
        M = cv.getPerspectiveTransform(pts2,pts1)
        dst = cv.warpPerspective(image,M,(cols,rows))
        return dst
    else:
        return image

def display(x):
    global current
    if x == "noise":
        gaussian = add_gaussian_noise(img)
        current = gaussian  
        dst = rotate_and_resize(gaussian)
    else:
        dst = rotate_and_resize(current)
    dst = projection(dst)
    dst = my_surf(dst)
    dst = np.uint8(dst)
    cv.imshow(window_title,dst)

def addPoint(event,x,y,flags,param):
    global nb_points_selectionnes
    if event == cv.EVENT_LBUTTONDOWN and nb_points_selectionnes<4:
        pts2[nb_points_selectionnes] = [x,y]
        nb_points_selectionnes += 1
        display("affichage de la zone s??lectionn??e")
    elif event == cv.EVENT_RBUTTONDOWN and nb_points_selectionnes>3:
        nb_points_selectionnes = 0
        display("Retour ?? l'image original")

def modificationNoise(x):
    display("noise")

cv.namedWindow(window_title)
cv.createTrackbar("Angle",window_title,0,360,display)
cv.createTrackbar("Scale",window_title,50,100,display)
cv.createTrackbar("Noise",window_title,2,20,modificationNoise)
cv.createTrackbar("Nb points",window_title,25,1000,display)
cv.setMouseCallback(window_title,addPoint)
display("initialisation")
if cv.waitKey(0):
    cv.destroyAllWindows()


