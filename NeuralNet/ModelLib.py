
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten

class ModelFactory:
    
    @staticmethod
    def createModel(image_size, nClasses, input_shape):
        model = Sequential()
        # The first two layers with 32 filters of window size 3x3
        model.add(Conv2D(image_size, (3, 3), padding='same', activation='relu', input_shape=input_shape))
        model.add(Conv2D(image_size, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(image_size * 2, (3, 3), padding='same', activation='relu'))
        model.add(Conv2D(image_size * 2, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Conv2D(image_size * 2, (3, 3), padding='same', activation='relu'))
        model.add(Conv2D(image_size * 2, (3, 3), activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        model.add(Flatten())
        model.add(Dense(image_size * 16, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(nClasses, activation='softmax'))
        
        return model