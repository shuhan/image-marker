import numpy as np
import cv2
import sys

if len(sys.argv) != 2:
    print("Usages: python cluster.py [input_image]")
    sys.exit()

image_file = sys.argv[1]

K = 8

origImg = cv2.imread(image_file)

img = cv2.cvtColor(origImg, cv2.COLOR_BGR2HSV)

Z = img.reshape((-1,3))

# convert to np.float32
Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_PP_CENTERS)

# Now convert back into uint8, and make original image
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

print(label)
print(center)

# cv2.imshow("Original", img)
cv2.imshow('res2', cv2.cvtColor(res2, cv2.COLOR_HSV2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()