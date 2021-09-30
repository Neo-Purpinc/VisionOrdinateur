import cv2 as cv
import sys
from matplotlib import pyplot as plt

if len(sys.argv) != 2:
    sys.exit("Image path missing.")

img = cv.imread(cv.samples.findFile(sys.argv[1]),cv.IMREAD_GRAYSCALE)
if img is None:
    sys.exit("Could not read the image.")
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cl2 = cv.equalizeHist(img)

histr = cv.calcHist([img],[0],None,[256],[0,256])
plt.figure("Greyscale Histogram")
plt.plot(histr)
plt.xlim([0,256])
plt.title("Greyscale Histogram")
plt.show(block=False)

histr_equalized = cv.calcHist(cl1,[0],None,[256],[0,256])
plt.figure("Greyscale Histogram (Equalized : CLAHE algorithm)")
plt.plot(histr_equalized)
plt.xlim([0,256])
plt.title("Greyscale Histogram (Equalized : CLAHE algorithm)")
plt.show(block=False)

histr_equalized2 = cv.calcHist(cl2,[0],None,[256],[0,256])
plt.figure("Greyscale Histogram (Equalized : equalizeHist)")
plt.plot(histr_equalized2)
plt.xlim([0,256])
plt.title("Greyscale Histogram (Equalized : equalizeHist)")
plt.show(block=False)


cv.imshow("Input image", img)
cv.imshow("Equalized image with CLAHE algorithm",cl1)
cv.imshow("Equalized image with opencv function : equalizeHist",cl2)
cv.waitKey(0)
