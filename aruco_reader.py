import numpy as np
import cv2
import sys
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

if len(sys.argv) != 2:
    print("Usages: python cluster.py [input_image]")
    sys.exit()

# image_file = sys.argv[1]

# frame = cv2.imread(image_file)
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters_create()
# corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
# frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

# plt.figure()
# plt.imshow(frame_markers)
# for i in range(len(ids)):
#     c = corners[i][0]
#     plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label = "id={0}".format(ids[i]))
# plt.legend()
# plt.show()

fig = plt.figure()
nx = 2
ny = 2
for i in range(1, nx*ny+1):
    ax = fig.add_subplot(ny,nx, i)
    img = aruco.drawMarker(aruco_dict, i, 700)
    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
    ax.axis("off")

plt.savefig("static/data/markers.pdf")
plt.show()