import numpy as np
import cv2 as cv
import sys

if len(sys.argv) != 3:
    print("Usage: python3 SIFT.py <filename1> <filename2>")
    sys.exit(1)

img_1 = cv.imread(sys.argv[1],cv.IMREAD_GRAYSCALE)
img_2 = cv.imread(sys.argv[2],cv.IMREAD_GRAYSCALE)
# Initiate SIFT detector
orb = cv.ORB_create()

kp_1, desc_1 = orb.detectAndCompute(img_1,None)
kp_2, desc_2 = orb.detectAndCompute(img_2,None)

img_1=cv.drawKeypoints(img_1,kp_1,img_1)
img_2=cv.drawKeypoints(img_2,kp_2,img_2)

bf = cv.BFMatcher()

matches = bf.knnMatch(desc_1, desc_2, k=2)
good_matches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:      
        good_matches.append(m)
src_pts = np.float32([ kp_1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)             #Gives us the index of the descriptor in the list of train descriptors 
dst_pts = np.float32([ kp_2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)               #Gives us the index of the descriptor in the list of query descriptors 

#homography relates the transformation between two plane by using RANSAC Algorithm
H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
matchesMask = mask.ravel().tolist()

ran_pts1 = []
ran_pts2 = []
for i in [np.random.randint(0,len(good_matches) -1 ) for x in range(10)] :
    ran_pts1.append(good_matches[i])
    ran_pts2.append(matchesMask[i])

#parameters to draw the 10 random points and only inliners
params = dict(matchColor = np.random.randint(low = 0, high = 255, size = 3).tolist(),
                   matchesMask = ran_pts2, # draw only inliners
                   flags = 2)

#Plotting keypoints for only 10 Inliers
img_4 = cv.drawMatches(img_1,kp_1,img_2,kp_2,ran_pts1,None,**params)
cv.imshow("task1_matches.jpg",img_4)

height,width = img_1.shape[:2]
pts = np.float32([ [0,0],[0,height-1],[width-1,height-1],[width-1,0] ]).reshape(-1,1,2)
#Taking the border points of the image(i.e Corner Points)
dst = cv.perspectiveTransform(pts,H)

#Extracting the rows and cols
rows1, cols1 = img_1.shape[:2]
rows2, cols2 = img_2.shape[:2]

#Getting Border Points
pts1 = np.float32([[0,0], [0,rows1], [cols1, rows1], [cols1,0]]).reshape(-1,1,2)
temp_points = np.float32([[0,0], [0,rows2], [cols2, rows2], [cols2,0]]).reshape(-1,1,2)

#Taking Perspective
pts2 = cv.perspectiveTransform(temp_points, H)
pts = np.concatenate((pts1, pts2), axis=0)

#For calculating the size of the output image
[x_min, y_min] = np.int32(pts.min(axis=0).ravel() - 0.5)
[x_max, y_max] = np.int32(pts.max(axis=0).ravel() + 0.5)

trans_dist = [-x_min, -y_min]

H_trans = np.array([[1, 0, trans_dist[0]], [0, 1, trans_dist[1]], [0,0,1]])
#Warping image 1 on top of Image 2
warp_img = cv.warpPerspective(img_1, H_trans.dot(H), (x_max - x_min, y_max - y_min))
warp_img[trans_dist[1]:rows1+trans_dist[1],trans_dist[0]:cols1+trans_dist[0]] = img_2
cv.imshow("Final",warp_img)

cv.waitKey(0)