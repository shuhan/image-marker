
import math
import matplotlib
import matplotlib.pyplot as plt
from keras.models import model_from_json
import numpy as np
import cv2
import sys

from NeuralNet.DroneData import Loader

model_file  = 'static/model/drone_vision_model.json'
weight_file = 'static/model/drone_vision_weight.h5'

if len(sys.argv) != 2:
    print("Usages: python run_cnn.py [input_image]")
    sys.exit()

image_file = sys.argv[1]

print("Processing:", image_file)

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

image = cv2.imread(image_file)

loader = Loader()

slices, cords  = loader.slice_image(image)

prediction = model.predict_classes(slices)

print(prediction)

overlay = image.copy()
output = image.copy()

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255)
]

alpha = 0.4

for i in range(0, len(cords)):
    cv2.rectangle(overlay, (cords[i][0], cords[i][1]), (cords[i][0] + 60, cords[i][1] + 60), colors[prediction[i]], -1)

# apply the overlay
cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
cv2.imshow("Output", output)
cv2.waitKey(0)

# Lesson learnt
# --------------------------------------------------
# Need more data and must balance the data set