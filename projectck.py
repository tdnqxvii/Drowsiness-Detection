# -*- coding: utf-8 -*-
"""ProjectCK.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bC0IrJDJ67HWI2MftXTptCEe2_2amWVH
"""

import numpy as np 
import pandas as pd 
import os
import cv2

import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout

# Define function to show image

def plot_imgs(dir, top=10):
    all_dirs = os.listdir(dir)
    path = [os.path.join(dir, file) for file in all_dirs][:5]
  
    plt.figure(figsize=(20, 20))
  
    for i, img_path in enumerate(path):
        plt.subplot(10, 10, i+1)
    
        img = plt.imread(img_path)
        plt.tight_layout()         
        plt.imshow(img, cmap='gray')

#Load data from drive

data_path = '/content/drive/MyDrive/AI/Sleep/train'

directories = ['/Closed', '/Open','/no_yawn', '/yawn']

for j in directories:
    plot_imgs(data_path+j)

batch_size = 40
img_height = 256
img_width = 256

## loading training data
training_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/drive/MyDrive/AI/Sleep/train',
    #validation_split=0.2,
    #subset= "training",
    seed=42,
    image_size= (img_height, img_width),
    batch_size=batch_size

)

## loading testing data
testing_ds = tf.keras.preprocessing.image_dataset_from_directory(
'/content/drive/MyDrive/AI/Sleep/test',
    #validation_split=0.2,
    #subset= "validation",
    seed=42,
    image_size= (img_height, img_width),
    batch_size=batch_size

)

## loading training data
training_ds = tf.keras.preprocessing.image_dataset_from_directory(
    '/content/drive/MyDrive/AI/Sleep/train',
    #validation_split=0.2,
    #subset= "training",
    seed=42,
    image_size= (img_height, img_width),
    batch_size=batch_size

)

## loading testing data
testing_ds = tf.keras.preprocessing.image_dataset_from_directory(
'/content/drive/MyDrive/AI/Sleep/test',
    #validation_split=0.2,
    #subset= "validation",
    seed=42,
    image_size= (img_height, img_width),
    batch_size=batch_size

)

class_names = training_ds.class_names
class_names

plt.figure(figsize=(10, 10))
for images, labels in training_ds.take(1):
  for i in range(12):
    ax = plt.subplot(3,4 , i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.grid(True)

# Create Model CNN with output

output = 4

model = Sequential()
model.add(Conv2D(32, (3,3), padding = 'same', kernel_initializer = 'he_uniform', input_shape = (256,256,3), activation = 'relu'))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(64, (3,3), padding = 'same',  kernel_initializer = 'he_uniform', activation = 'relu'))
model.add(MaxPooling2D(2,2))

model.add(Conv2D(128,(3,3), padding='same',  kernel_initializer = 'he_uniform', activation='relu'))
model.add(MaxPooling2D(2,2))

model.add(Flatten())

model.add(Dense(64, activation = 'relu',  kernel_initializer = 'he_uniform'))

model.add(Dense(output, activation = 'softmax'))

model.summary()

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])

history = model.fit(training_ds, validation_data= testing_ds, epochs = 20)

model.save('/content/drive/MyDrive/AI/modelNQ.h5')

# Load model
from keras.models import load_model
model = load_model('/content/drive/MyDrive/AI/modelnua.h5')

score = model.evaluate(testing_ds, verbose = 1)

print('Test loss = ', score[0])
print('Test acuaracy = ',score[1])

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','validation'])

from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import array_to_img
import numpy as np
import cv2
from google.colab.patches import cv2_imshow

filename = '2.jpg'
anh = cv2.imread(filename)
image = cv2.resize(anh, (256, 256)) 
cv2_imshow(image)
tensor = np.expand_dims(image, axis=0)
results = model.predict(tensor)
label = int(np.argmax(results, axis = 1))

print(class_names[label])

plt.figure(figsize=(20, 20))
for images, labels in testing_ds.take(2):
    predictions = model.predict(images)
    predlabel = []    
    for mem in predictions:
        predlabel.append(class_names[np.argmax(mem)])    
    for i in range(20):
        ax = plt.subplot(5,4,i+1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title('Predicted label:'+ predlabel[i])
        plt.axis('off')
        plt.grid(True)

