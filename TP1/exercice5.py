
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Real-time histograms')
ax1.set_title('Gray histogram')
ax2.set_title('RGB histogram')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    gray_3channels = np.stack((gray,)*3, axis=-1)
    concatenate = np.concatenate((frame, gray_3channels), axis=0)
    
    h,s,v = cv.split(hsv)
    equalized_v = cv.equalizeHist(v)
    v_hsv = cv.merge((h,s,equalized_v))
    concatenate_hsv = np.concatenate((hsv,v_hsv),axis=1)

    plt.subplot(211),plt.title('Gray histogram'),plt.hist(gray.ravel(),256,[0,256],color="gray")
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv.calcHist([frame],[i],None,[256],[0,256])
        plt.subplot(212),plt.plot(histr,color = col)
    plt.subplot(212),plt.title('RGB histogram')
    
    plt.show(block=False)
    cv.imshow('RGB & Gray',concatenate)
    cv.imshow('Before & After Equalization',concatenate_hsv)

    plt.pause(0.1)
    plt.clf()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
