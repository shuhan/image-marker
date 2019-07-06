# Ugly hack to allow absolute import from the root folder
# whatever its name is. Please forgive the heresy.
if __name__ == "__main__" and __package__ is None:
    from sys import path
    from os.path import dirname as dir

    path.append(dir(path[0]))

import numpy as np
import cv2

from NeuralNet.DroneData import Loader

loader = Loader('static/marked/')

(train_images, train_labels), (test_images, test_labels)  = loader.load_data()

print('Training data shape : ', train_images.shape, train_labels.shape)
print('Testing data shape : ', test_images.shape, test_labels.shape)

(train_images, train_labels), (test_images, test_labels)  = loader.balance_data()

print('Training data shape : ', train_images.shape, train_labels.shape)
print('Testing data shape : ', test_images.shape, test_labels.shape)

unique, count = np.unique(train_labels, return_counts=True)

print(unique)
print(count)

loader.balance_data()

image = cv2.imread('static/flight_capture/2019-06-21-19:15:22.png')

grids, cords = loader.slice_image(image)

print(cords)