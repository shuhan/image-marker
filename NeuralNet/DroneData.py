import os
import cv2
import random
import json
import numpy as np
import math

from NeuralNet.LabelDict import Dictionary as LDict

class Loader:

    def __init__(self, dirname, grid_size=60, training_ratio=0.8, test_ratio=0.2, labels=['Obstacle', 'MR.York', 'Vehicle', 'Wall', 'Floor', 'RescueVehicle']):

        actual_training_ratio  = training_ratio / (training_ratio + test_ratio)
        actual_test_ratio   = test_ratio / (training_ratio + test_ratio)
        if not os.path.isdir(dirname):
            raise NotADirectoryError
        self.data_dir                   = dirname
        self.grid_size                  = grid_size
        self.training_ratio             = actual_training_ratio
        self.test_ratio                 = actual_test_ratio
        self.dict                       = LDict(labels)
        self.data_loaded                = False
        self.training_images            = []
        self.training_labels            = []
        self.test_images                = []
        self.test_labels                = []
        self.data_balanced              = False
        self.balanced_training_images   = []
        self.balanced_training_labels   = []
        self.balanced_test_images       = []
        self.balanced_test_labels       = []

    def _process_image(self, image_file, config_file):
        '''
        process for each image
        '''
        print("Processing {} ...".format(image_file)),
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
        print('done')

    def load_data(self):

        if self.data_loaded:
            return (np.array(self.training_images), np.array(self.training_labels)), (np.array(self.test_images), np.array(self.test_labels))
        self.data_loaded    = True

        filelist = os.listdir(self.data_dir)
        for filename in filelist:
            if filename.endswith(".png"):
                self._process_image(os.path.join(self.data_dir, filename), os.path.join(self.data_dir, os.path.splitext(filename)[0] + '.json'))

        return (np.array(self.training_images), np.array(self.training_labels)), (np.array(self.test_images), np.array(self.test_labels))

    def balance_data(self):
        '''
        Balance the loaded dataset and return it. load_data must be called before balance_data can be used.
        '''
        if self.data_balanced:
            return (np.array(self.balanced_training_images), np.array(self.balanced_training_labels)), (np.array(self.balanced_test_images), np.array(self.balanced_test_labels))
        self.data_balanced  = True

        if not self.data_loaded:
            self.load_data()

        unique, counts = np.unique(self.training_labels, return_counts=True)
        total = np.sum(counts)
        likelyhood = (total - counts)/total

        for i in range(0, len(self.training_labels)):
            dice    = random.random()
            label   = self.training_labels[i]
            image   = self.training_images[i]

            if dice < likelyhood[np.where(unique==label)]:
                self.balanced_training_images.append(image)
                self.balanced_training_labels.append(label)

        for i in range(0, len(self.test_labels)):
            dice    = random.random()
            label   = self.test_labels[i]
            image   = self.test_images[i]

            if dice < likelyhood[np.where(unique==label)]:
                self.balanced_test_images.append(image)
                self.balanced_test_labels.append(label)

        return (np.array(self.balanced_training_images), np.array(self.balanced_training_labels)), (np.array(self.balanced_test_images), np.array(self.balanced_test_labels))

    def slice_image(self, image):
        '''
        Process given image and prepare a list of inputs for evaluation.
        '''
        height, width, channels = image.shape

        self.height     = height
        self.width      = width
        self.channels   = channels

        self.cols       = math.floor(self.width / self.grid_size)
        self.rows       = math.floor(self.height / self.grid_size)

        self.x_offset   = int((self.width - (self.cols * self.grid_size)) / 2)
        self.y_offset   = int((self.height - (self.rows * self.grid_size)) / 2)

        grids = []
        cords = []

        for r in range(0, self.rows):
            for c in range(0, self.cols):
                x = self.x_offset + (c * self.grid_size)
                y = self.y_offset + (r * self.grid_size)

                cropped_img = image[y:y+self.grid_size, x:x+self.grid_size]

                grids.append(cropped_img)
                cords.append([x, y])
        
        return np.array(grids), np.array(cords)
