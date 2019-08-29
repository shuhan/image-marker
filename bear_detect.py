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

bear_mask   = cv2.inRange(hsvImage, np.array([10, 110, 64]), np.array([32, 176, 155])) & (expect_mask * 255)
tshirt_mask = cv2.inRange(hsvImage, np.array([40, 51, 26]), np.array([77, 95, 61])) & (expect_mask * 255)

# bear_mask   = cv2.inRange(hsvImage, np.array([16, 64, 60]), np.array([30, 150, 130])) & (expect_mask * 255)
# tshirt_mask = cv2.inRange(hsvImage, np.array([40, 40, 32]), np.array([75, 113, 66])) & (expect_mask * 255)

kernel = np.ones((16,16),np.uint8)

_, bear_mask = cv2.threshold(cv2.blur(bear_mask, (5,5)), 127, 255, cv2.THRESH_BINARY)

_, tshirt_mask = cv2.threshold(cv2.blur(tshirt_mask, (5,5)), 127, 255, cv2.THRESH_BINARY)
tshirt_region = cv2.dilate(tshirt_mask, kernel, iterations=2)

bear_found = np.sum(np.bitwise_and(bear_mask, tshirt_region)) > threash

if bear_found:
    im2, contours, hierarchy = cv2.findContours(tshirt_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    accepted_contures = []
    
    for contour in contours:
        contour = cv2.convexHull(contour)
        x,y,w,h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        wh_ratio = float(w)/float(h)
        
        if area > threash and area > 0.6 * w * h and wh_ratio > 0.7 and wh_ratio < 1.40 and np.sum(bear_mask[y:y+h, x:x+w])/255 > threash:
            accepted_contures.append(contour)
            cv2.rectangle(origImg, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    cv2.imshow("Bear Found", origImg)

cv2.waitKey(0)
