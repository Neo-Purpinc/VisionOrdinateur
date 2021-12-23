import numpy as np
import cv2 as cv
import sys
import os
import argparse
def getArgs():
    parser = argparse.ArgumentParser(description='This program stitch a folder of images into a panorama using SIFT.')
    parser.add_argument('--input', type=str, help='Path to a folder of images.', default='img/')
    parser.add_argument('--output',type=str,help="Path to the output image file.", default='Output/panorama.jpg')
    parser.add_argument('--algo', type=str, help='Background subtraction method (SIFT,ORB,Stitcher).', default='SIFT')
    return parser

def initialize():
    args = getArgs().parse_args()
    directory = args.input
    files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory,filename)
        files.append(f)
    files.sort()
    imgs = []
    for i in range(len(files)):
        imgs.append(cv.imread(files[i],cv.IMREAD_COLOR))
    return imgs,args

def completeImages(img1,img2):
    if(img1.shape!=img2.shape):
        maxHeight = img1.shape[0] if img1.shape[0] >= img2.shape[0] else img2.shape[0]
        maxWidth = img1.shape[1] if img1.shape[1] >= img2.shape[1] else img2.shape[1]
        img1 = cv.copyMakeBorder(img1, 0, maxHeight - img1.shape[0], 0, maxWidth - img1.shape[1], cv.BORDER_CONSTANT, value=[0,0,0])
        img2 = cv.copyMakeBorder(img2, 0, maxHeight - img2.shape[0], 0, maxWidth - img2.shape[1], cv.BORDER_CONSTANT, value=[0,0,0])
    return img1,img2

def warpImages(img1,img2,H):
    rows1, cols1 = img1.shape[:2]
    rows2, cols2 = img2.shape[:2]

    list_of_points_1 = np.float32([[0,0], [0,rows1], [cols1,rows1], [cols1,0]]).reshape(-1,1,2)
    temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)
    list_of_points_2 = cv.perspectiveTransform(temp_points, H)
    list_of_points = np.concatenate((list_of_points_1, list_of_points_2), axis=0)

    [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
    [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
    translation_dist = [-x_min, -y_min]
    H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0,0,1]]) 

    output_img = cv.warpPerspective(img1, H_translation.dot(H), (x_max-x_min, y_max-y_min))
    output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img2
    
    return output_img

def stitch2images(img_1,img_2):

    kp_1, desc_1 = algo.detectAndCompute(img_1,None)
    kp_2, desc_2 = algo.detectAndCompute(img_2,None)
    
    matches = bf.knnMatch(desc_1, desc_2, k=2)
    good_matches = []
    for m,n in matches:
        if m.distance < 0.5*n.distance:      
            good_matches.append(m)
    src_pts = np.float32([ kp_1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp_2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)

    H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)
    img_1_completed, img_2_completed = completeImages(img_1,img_2)
    warp_img = warpImages(img_1_completed,img_2_completed,H)
    return warp_img

imgs,args = initialize()
algo_to_use = args.algo.upper()
if(algo_to_use=='SIFT'or algo_to_use=='ORB'):
    if(algo_to_use=='SIFT'):
        algo = cv.SIFT_create()
    else:
        algo = cv.ORB_create()
    bf = cv.BFMatcher()
    res = imgs[0]
    for i in range(1,8):
        currentImg = imgs[i]
        res = stitch2images(res,currentImg)
    res = cv.resize(res,(1200,720))
else:
    print("Using Stitcher")
    algo = cv.Stitcher.create(cv.Stitcher_PANORAMA)
    status,pano = algo.stitch(imgs)
    res = cv.resize(pano,(pano.shape[1]//2,pano.shape[0]//2))
cv.imshow("Final",res)
cv.waitKey(0)