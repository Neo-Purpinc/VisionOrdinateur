import cv2 as cv
import sys
from matplotlib import pyplot as plt

if len(sys.argv) != 2:
    sys.exit("Image path missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_COLOR)
if img is None:
    sys.exit("Could not read the image.")
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

b,g,r = cv.split(img)
equalized_b = cv.equalizeHist(b)
equalized_g = cv.equalizeHist(g)
equalized_r = cv.equalizeHist(r)
separate_channels_img = cv.merge((equalized_b,equalized_g,equalized_r))

h,s,v = cv.split(hsv)
equalized_v = cv.equalizeHist(v)
v_img = cv.merge((h,s,equalized_v))

color = ('b','g','r')
plt.figure("Method 1 : BEFORE EQUALIZING")
for i,col in enumerate(color):
    histr_separate_channels = cv.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr_separate_channels,color = col)
    plt.xlim([0,256])
plt.title("Separate channels method : Histogram")
plt.show(block=False)

color = ('h','s','v')
plt.figure("Method 2 : BEFORE EQUALIZING")
for i,col in enumerate(color):
    histr_value  = cv.calcHist([hsv],[i],None,[256],[0,256])
    plt.plot(histr_value)
    plt.xlim([0,256])
plt.title("Value channel method : Histogram")
plt.show(block=False)

color = ('b','g','r')
plt.figure("Method 1 : AFTER EQUALIZING")
for i,col in enumerate(color):
    histr_separate_channels_equalized = cv.calcHist([separate_channels_img],[i],None,[256],[0,256])
    plt.plot(histr_separate_channels_equalized,color = col)
    plt.xlim([0,256])
plt.title("Separate channels method : Equalized Histogram")
plt.show(block=False)

color = ('h','s','v')
plt.figure("Method 2 : AFTER EQUALIZING")
for i,col in enumerate(color):
    histr_value_equalized  = cv.calcHist([v_img],[i],None,[256],[0,256])
    plt.plot(histr_value_equalized)
    plt.xlim([0,256])
plt.title("Value channel method : Equalized Histogram")
plt.show(block=False)
cv.imshow("Original RGB Image", img)
cv.imshow("Original HSV Image", hsv)
cv.imshow("Equalized RGB Image", separate_channels_img)
cv.imshow("Equalized HSV Image", v_img)
cv.waitKey(0)
