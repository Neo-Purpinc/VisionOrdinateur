import numpy as np
import cv2 as cv
import sys
import os

if len(sys.argv) != 2:
    print("Usage: python3 SIFT.py <directory>")
    sys.exit(1)
directory = sys.argv[1]
files = []
for filename in os.listdir(directory):
    f = os.path.join(directory,filename)
    files.append(f)
files.sort()

sift = cv.SIFT_create()
bf = cv.BFMatcher()

def stitch2images(img_1,img_2):
    kp_1, desc_1 = sift.detectAndCompute(img_1,None)
    kp_2, desc_2 = sift.detectAndCompute(img_2,None)
    
    matches = bf.knnMatch(desc_1, desc_2, k=2)
    good_matches = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:      
            good_matches.append(m)
    src_pts = np.float32([ kp_1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)             #Gives us the index of the descriptor in the list of train descriptors 
    dst_pts = np.float32([ kp_2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)               #Gives us the index of the descriptor in the list of query descriptors 

    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    ran_pts1 = []
    ran_pts2 = []
    for i in [np.random.randint(0,len(good_matches) -1 ) for x in range(10)] :
        ran_pts1.append(good_matches[i])
        ran_pts2.append(matchesMask[i])


    height,width = img_1.shape[:2]
    pts = np.float32([ [0,0],[0,height-1],[width-1,height-1],[width-1,0] ]).reshape(-1,1,2)

    dst = cv.perspectiveTransform(pts,H)

    rows1, cols1 = img_1.shape[:2]
    rows2, cols2 = img_2.shape[:2]

    pts1 = np.float32([[0,0], [0,rows1], [cols1, rows1], [cols1,0]]).reshape(-1,1,2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2, rows2], [cols2,0]]).reshape(-1,1,2)

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
    return warp_img


print(files)
# res = cv.imread(files[0],cv.IMREAD_COLOR)
# for i in range(len(files)):
#     current = cv.imread(files[i],cv.IMREAD_COLOR)
#     res = stitch2images(res,current)

res = stitch2images(cv.imread(files[0]),cv.imread(files[1]))
res = stitch2images(res,cv.imread(files[2]))
cv.imshow("Final",res)
cv.waitKey(0)