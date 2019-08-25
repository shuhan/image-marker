import numpy as np
import cv2
import sys
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

# if len(sys.argv) != 2:
#     print("Usages: python cluster.py [input_image]")
#     sys.exit()

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

# Groud Robot Markers 1, 2, 3, 4
fig1 = plt.figure()
ax = fig1.add_subplot(1, 1, 1)
img = aruco.drawMarker(aruco_dict, 1, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.savefig("static/data/ground-robot.pdf")

# MR York Vehicle Marker 10
fig2 = plt.figure()
ax = fig2.add_subplot(1, 2, 1)
img = aruco.drawMarker(aruco_dict, 10, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")

ax = fig2.add_subplot(1, 2, 2)
img = aruco.drawMarker(aruco_dict, 10, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.savefig("static/data/mr-york.pdf")

# Landing Pad
fig3 = plt.figure()
ax = fig3.add_subplot(1, 1, 1)
img = aruco.drawMarker(aruco_dict, 40, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.savefig("static/data/landing-pad.pdf")

fig4 = plt.figure()
ax = fig4.add_subplot(1, 1, 1)
img = aruco.drawMarker(aruco_dict, 39, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.savefig("static/data/east-entry.pdf")

fig5 = plt.figure()
ax = fig5.add_subplot(1, 1, 1)
img = aruco.drawMarker(aruco_dict, 41, 700)
plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
ax.axis("off")
plt.savefig("static/data/north-entry.pdf")


plt.show()