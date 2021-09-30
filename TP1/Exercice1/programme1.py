import cv2 as cv
import sys

if len(sys.argv) != 2:
    sys.exit("Image path missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]))
if img is None:
    sys.exit("Could not read the image.")
dimensions = img.shape
height = dimensions[0]
width = dimensions[1]
channels = dimensions[2]
print("Hauteur : ",height)
print("Largeur : ",width)
print("Nombre de canaux : ",channels)
b,g,r = cv.split(img)
grey_blue = cv.merge((b,b,b))
grey_green = cv.merge((g,g,g))
grey_red = cv.merge((r,r,r))
cv.imshow("Original Image", img)
cv.imshow("Grey from blue channel", grey_blue)
cv.imshow("Grey from green channel", grey_green)
cv.imshow("Grey from red channel", grey_red)

hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
h,s,v = cv.split(hsv)
grey_hue  = cv.merge((h,h,h))
grey_saturation = cv.merge((s,s,s))
grey_value = cv.merge((v,v,v))
cv.imshow("Original HSV Image", hsv)
cv.imshow("Grey from hue channel", grey_hue)
cv.imshow("Grey from saturation channel", grey_saturation)
cv.imshow("Grey from value channel", grey_value)
cv.imwrite("grey_value.png",grey_value)
k = cv.waitKey(0)
