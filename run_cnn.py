
import math
import matplotlib
import matplotlib.pyplot as plt
from keras.models import model_from_json
import numpy as np
import cv2

from NeuralNet.DroneData import Loader

model_file  = 'static/data/drone_vision_model.json'
weight_file = 'static/data/drone_vision_weight.h5'

# load json and create model
json_file = open(model_file, 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(weight_file)
print("Model loaded from disk")
 
# evaluate loaded model on test data
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

loader = Loader('static/marked/')

(train_images, train_labels), (test_images, test_labels)  = loader.load_data()

print('Training data shape : ', train_images.shape, train_labels.shape)
print('Testing data shape : ', test_images.shape, test_labels.shape)


prediction = model.predict_classes(test_images[0:40])

print(prediction)
print(test_labels[0:40,0])

# Lesson learnt
# --------------------------------------------------
# Need more data and must balance the data set