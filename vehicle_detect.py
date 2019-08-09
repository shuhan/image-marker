import numpy as np
import cv2
import sys

if len(sys.argv) != 2:
    print("Usages: python object_detect.py [input_image]")
    sys.exit()

image_file = sys.argv[1]

origImg     = cv2.imread(image_file)
hsvImage    = cv2.cvtColor(origImg, cv2.COLOR_BGR2HSV)

floor_mask  = cv2.inRange(hsvImage, np.array([0, 0, 120]), np.array([100, 90, 210]))

height, width = floor_mask.shape

# filter anything above large block for not floor as not floor
normalized_mask = floor_mask/255

indices = range(height)
indices.reverse()

expect_mask = np.zeros(floor_mask.shape, normalized_mask.dtype)

for i in indices:
    if sum(normalized_mask[i, :]) < width/2:
        last_index = i
        break
    else:
        expect_mask[i, :] = np.ones((1, width), normalized_mask.dtype)

threash = 90

vheilce_mask = cv2.inRange(hsvImage, np.array([0, 100, 85]), np.array([10, 255, 125])) & expect_mask

kernel = np.ones((8,8),np.uint8)

vheilce_region = cv2.dilate(vheilce_mask, kernel, iterations=2)

vheilce_found = np.sum(vheilce_mask) > threash

if vheilce_found:
    im2, contours, hierarchy = cv2.findContours(vheilce_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    accepted_contures = []
    
    for contour in contours:
        contour = cv2.convexHull(contour)
        x,y,w,h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        wh_ratio = float(w)/float(h)
        
        if area > threash and area > 0.6 * w * h and wh_ratio > 0.7 and wh_ratio < 1.40 and np.sum(expect_mask[y:y+h, x:x+w]) > (2*area)/3:
            accepted_contures.append(contour)
            cv2.rectangle(origImg, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
cv2.imshow("Vehicle Found", origImg)
cv2.imshow("Vehicle Mask", vheilce_mask)
cv2.imshow("Vehicle Region", vheilce_region)

cv2.waitKey(0)
