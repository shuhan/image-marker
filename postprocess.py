#!/usr/bin/env python3

import os
import sys
import json
import cv2

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
        with open(config_file, 'r') as json_file:
            config = json.loads(json_file.read())
            
            print(config['url'])

            im = cv2.imread(image_file)


if __name__ == "__main__":
    PostProcess().process()
