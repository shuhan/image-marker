#!/usr/bin/env python3

import os
import sys
import json
import cv2
import random

class PostProcess:

    def __init__(self):
        '''
        Initialize the directories
        '''
        if len(sys.argv) != 3:
            self.help()

        self.training_ratio     = 0.6
        self.validation_ratio   = 0.2
        self.test_validation    = 0.2
        self.in_dir     = sys.argv[1]
        self.out_dir    = sys.argv[2]

        if not os.path.isdir(self.in_dir):
            self.help()

        if not os.path.isdir(self.out_dir):
            try:
                os.makedirs(self.out_dir)
            except OSError:
                pass

    def help(self):
        print("Usages: python postprocess.py [input_dir] [output_dir]")
        sys.exit()

    def process(self):
        '''
        Crope the images and store them in a seperate directory
        '''
        filelist = os.listdir(self.in_dir)
        for filename in filelist:
            if filename.endswith(".png"):
                self.process_image(os.path.join(self.in_dir, filename), os.path.join(self.in_dir, os.path.splitext(filename)[0] + '.json'))

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
            cols        = (width - (2*x_offset))/grid_size
            rows        = (height - (2*y_offset))/grid_size

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

                    rolled_value = random.random()

                    if rolled_value < self.training_ratio:
                        set_name = 'training'
                    elif rolled_value < self.training_ratio + self.validation_ratio:
                        set_name = 'validation'
                    else:
                        set_name = 'test'

                    file_dir    = os.path.join(self.out_dir, set_name, cname)
                    file_path   = os.path.join(file_dir, os.path.splitext(config['url'])[0] + '-' + index + '.png')

                    if not os.path.isdir(file_dir):
                        os.makedirs(file_dir)

                    cropped_img = im[y:y+grid_size, x:x+grid_size]
                    cv2.imwrite(file_path, cropped_img)
        print('Done')

if __name__ == "__main__":
    PostProcess().process()
