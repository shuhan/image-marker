import os
import cv2
import random
import json
import numpy as np

from LabelDict import Dictionary as LDict

class Loader:

    def __init__(self, dirname, training_ratio=0.8, test_ratio=0.2, labels=['Obstacle', 'MR.York', 'Vehicle', 'Wall', 'RescueVehicle', 'Floor']):

        actual_training_ratio  = training_ratio / (training_ratio + test_ratio)
        actual_test_ratio   = test_ratio / (training_ratio + test_ratio)
        if not os.path.isdir(dirname):
            raise NotADirectoryError
        self.data_dir       = dirname
        self.training_ratio = actual_training_ratio
        self.test_ratio     = actual_test_ratio
        self.dict           = LDict(labels)

    def process_image(self, image_file, config_file):
        '''
        process for each image
        '''
        print("Processing {} ... ".format(image_file)),
        with open(config_file, 'r') as json_file:
            config = json.loads(json_file.read())
            
            grid_size   = config['karnel_size']
            x_offset    = config['start_left']
            y_offset    = config['start_top']
            width       = config['width']
            height      = config['height']
            cols        = int((width - (2*x_offset))/grid_size)
            rows        = int((height - (2*y_offset))/grid_size)

            im = cv2.imread(image_file)

            for r in range(0, rows):
                for c in range(0, cols):
                    seq     = (r * cols) + c
                    index   = str(seq)
                    if len(config['marks'][index]) > 1:
                        continue
                    cname = config['marks'][index][0]
                    x = x_offset + (c * grid_size)
                    y = y_offset + (r * grid_size)

                    cropped_img = im[y:y+grid_size, x:x+grid_size]

                    rolled_value = random.random()

                    if rolled_value < self.training_ratio:
                        self.training_images.append(cropped_img)
                        self.training_labels.append([self.dict.getIndex(cname)])
                    else:
                        self.test_images.append(cropped_img)
                        self.test_labels.append([self.dict.getIndex(cname)])

    def load_data(self):

        self.training_images     = []
        self.training_labels     = []
        self.test_images         = []
        self.test_labels         = []

        filelist = os.listdir(self.data_dir)
        for filename in filelist:
            if filename.endswith(".png"):
                self.process_image(os.path.join(self.data_dir, filename), os.path.join(self.data_dir, os.path.splitext(filename)[0] + '.json'))

        return (np.array(self.training_images), np.array(self.training_labels)), (np.array(self.test_images), np.array(self.test_labels))

