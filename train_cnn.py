from __future__ import print_function

import os
import sys

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import keras
from keras.utils import to_categorical
import cv2

from NeuralNet.DroneData import Loader
from NeuralNet.ModelLib import ModelFactory

class TrainCNN:

    def __init__(self):
        '''
        Initialize the directories
        '''
        if len(sys.argv) != 3:
            self.help()
        
        self.in_dir     = sys.argv[1]
        self.model_dir  = sys.argv[2]

        if not os.path.isdir(self.in_dir):
            self.help()
        if not os.path.isdir(self.model_dir):
            try:
                os.makedirs(self.model_dir)
            except OSError:
                pass
        self.model_file     = os.path.join(self.model_dir, 'drone_vision_model.json')
        self.weight_file    = os.path.join(self.model_dir, 'drone_vision_weight.h5')
        self.batch_size     = 256
        self.epochs         = 10

    def help(self):
        print("Usages: python train_cnn.py [input_dir] [model_dir]")
        sys.exit()

    def train(self):
        '''
        Train load data and train the network
        '''
        loader = Loader(self.in_dir)

        (train_images, train_labels), (test_images, test_labels)  = loader.load_data()
        
        print('Training data shape : ', train_images.shape, train_labels.shape)
        print('Testing data shape : ', test_images.shape, test_labels.shape)

        classes     = loader.dict.classes()
        nClasses    = loader.dict.count()
        print('Total number of outputs : ', nClasses)
        print('Output classes : ', classes)

        plt.figure(figsize=[4,2])

        # Display the first image in training data
        plt.subplot(121)
        plt.imshow(train_images[0,:,:], cmap='gray')
        plt.title("Ground Truth : {}".format(train_labels[0]))

        # Display the first image in testing data
        plt.subplot(122)
        plt.imshow(test_images[0,:,:], cmap='gray')
        plt.title("Ground Truth : {}".format(test_labels[0]))

        # Find the shape of input images and create the variable input_shape
        nRows,nCols,nDims = train_images.shape[1:]
        train_data = train_images.reshape(train_images.shape[0], nRows, nCols, nDims)
        test_data = test_images.reshape(test_images.shape[0], nRows, nCols, nDims)
        input_shape = (nRows, nCols, nDims)

        # Change to float datatype
        train_data = train_data.astype('float32')
        test_data = test_data.astype('float32')

        # Scale the data to lie between 0 to 1
        train_data /= 255
        test_data /= 255

        # Change the labels from integer to categorical data
        train_labels_one_hot = to_categorical(train_labels)
        test_labels_one_hot = to_categorical(test_labels)

        print('Original label 0 : ', train_labels[0])
        print('After conversion to categorical ( one-hot ) : ', train_labels_one_hot[0])

        model = ModelFactory.createModel(nRows, nClasses, input_shape)
        model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        model.summary()

        history = model.fit(train_data, train_labels_one_hot, batch_size=self.batch_size, epochs=self.epochs, verbose=1, 
                   validation_data=(test_data, test_labels_one_hot))
        model.evaluate(test_data, test_labels_one_hot)


        # serialize model to JSON
        model_json = model.to_json()
        with open(self.model_file, "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights(self.weight_file)
        print("Saved model to disk")

        plt.figure(figsize=[8,6])
        plt.plot(history.history['loss'],'r',linewidth=3.0)
        plt.plot(history.history['val_loss'],'b',linewidth=3.0)
        plt.legend(['Training loss', 'Validation Loss'],fontsize=18)
        plt.xlabel('Epochs ',fontsize=16)
        plt.ylabel('Loss',fontsize=16)
        plt.title('Loss Curves',fontsize=16)

        plt.figure(figsize=[8,6])
        plt.plot(history.history['acc'],'r',linewidth=3.0)
        plt.plot(history.history['val_acc'],'b',linewidth=3.0)
        plt.legend(['Training Accuracy', 'Validation Accuracy'],fontsize=18)
        plt.xlabel('Epochs ',fontsize=16)
        plt.ylabel('Accuracy',fontsize=16)
        plt.title('Accuracy Curves',fontsize=16)

        print("Training Complete")

        plt.show()

if __name__ == "__main__":
    TrainCNN().train()


