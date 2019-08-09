import numpy as np
import cv2
import sys

image_file = sys.argv[1]

origImg     = cv2.imread(image_file)
hsvImage    = cv2.cvtColor(origImg, cv2.COLOR_BGR2HSV)

lower_bound = np.array([14, 49, 71])
upper_bound = np.array([30, 128, 130])

# Bear
#---------------------
# 16, 64, 60
# 30, 150, 130
#---------------------
# t-shirt
#---------------------
# 40, 40, 32
# 75, 113, 66
#---------------------
# Floor Mask
#---------------------
# 0, 0, 120
# 100, 90, 210

mask = cv2.inRange(hsvImage, lower_bound, upper_bound)

threash     = 100
bear_mask   = cv2.inRange(hsvImage, np.array([6, 40, 40]), np.array([30, 140, 131]))
tshirt_mask = cv2.inRange(hsvImage, np.array([40, 40, 32]), np.array([75, 113, 66]))
floor_mask  = cv2.inRange(hsvImage, np.array([0, 0, 120]), np.array([100, 90, 210]))

#Erode the possible tshirt mask onece and then dialate it 10 times to create a bigger region
kernel = np.ones((5,5),np.uint8)
_, tshirt_mask = cv2.threshold(cv2.blur(tshirt_mask, (5,5)), 127, 255, cv2.THRESH_BINARY)
tshirt_region = cv2.dilate(tshirt_mask, kernel, iterations=10)

#Does the region also covers bear mask
bear_found = np.sum(np.bitwise_and(bear_mask, tshirt_region)) > threash and np.sum(np.bitwise_and(floor_mask, tshirt_region)) > threash

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel       = origImg[y, x]
        hsv_pixel   = hsvImage[y, x]
        print('BGR :'),
        print(pixel)
        print('HSV :'),
        print(hsv_pixel)

if len(sys.argv) != 2:
    print("Usages: python edge.py [input_image]")
    sys.exit()

cv2.namedWindow("Original Image")
cv2.setMouseCallback("Original Image", on_click)
cv2.imshow("Original Image", origImg)

cv2.imshow("bear_mask", bear_mask | tshirt_region)

def on_trackbar(val):
    lh = cv2.getTrackbarPos('lower H','Controller')
    ls = cv2.getTrackbarPos('lower S','Controller')
    lv = cv2.getTrackbarPos('lower V','Controller')

    uh = cv2.getTrackbarPos('upper H','Controller')
    us = cv2.getTrackbarPos('upper S','Controller')
    uv = cv2.getTrackbarPos('upper V','Controller')

    lower_bound = np.array([lh, ls, lv])
    upper_bound = np.array([uh, us, uv])

    mask = cv2.inRange(hsvImage, lower_bound, upper_bound)

    cv2.imshow("mask", mask)

cv2.namedWindow('Controller')
# create trackbars for color change
cv2.createTrackbar('lower H', 'Controller', lower_bound[0], 180, on_trackbar)
cv2.createTrackbar('lower S', 'Controller', lower_bound[1], 255, on_trackbar)
cv2.createTrackbar('lower V', 'Controller', lower_bound[2], 255, on_trackbar)

cv2.createTrackbar('upper H', 'Controller', upper_bound[0], 180, on_trackbar)
cv2.createTrackbar('upper S', 'Controller', upper_bound[1], 255, on_trackbar)
cv2.createTrackbar('upper V', 'Controller', upper_bound[2], 255, on_trackbar)

final_region = cv2.erode(cv2.dilate(np.bitwise_and(floor_mask, tshirt_region), kernel, iterations=1), kernel, iterations=1)

cv2.imshow("region", final_region)

if bear_found:
    im2, contours, hierarchy = cv2.findContours(final_region, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    accepted_contures = []
    
    for contour in contours:
        contour = cv2.convexHull(contour)
        x,y,w,h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        wh_ratio = float(w)/float(h)
        
        if area > threash and area > 0.6 * w * h and np.sum(final_region[y:y+h, x:x+w])/255 > (w * h)/3 and wh_ratio > 0.7 and wh_ratio < 1.40:
            accepted_contures.append(contour)

            cv2.rectangle(origImg, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #cv2.drawContours(origImg, accepted_contures, -1, (0,255,0), 3)
    cv2.imshow("Bear Found", origImg)

cv2.waitKey(0)
