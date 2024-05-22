from keras import layers, utils, Sequential, losses
import matplotlib as plt
import tensorflow as tf
import pandas as pd
import numpy as np

validation_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Fruits_Vegetables\\validation"
train_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Fruits_Vegetables\\train"
test_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Fruits_Vegetables\\test"

image_width = 180
image_height = 180

data_train = utils.image_dataset_from_directory(train_path, shuffle=True, image_size=(image_width, image_height), batch_size=32, validation_split=False)
category = data_train.class_names

data_validation = utils.image_dataset_from_directory(validation_path, shuffle=False, image_size=(image_width, image_height), batch_size=32, validation_split=False)
data_test = utils.image_dataset_from_directory(test_path, shuffle=False, image_size=(image_width, image_height), batch_size=32, validation_split=False)
                        # v Ajuste de cores                 # 1º Neurônios 2º RGB
model = Sequential([layers.Rescaling(1./255), layers.Conv2D(16, 3, padding='same', activation='relu'), 
                    layers.MaxPooling2D(), layers.Conv2D(32, 3, padding='same', activation='relu'),
                    layers.MaxPooling2D(), layers.Conv2D(64, 3, padding='same', activation='relu'),
                    layers.MaxPooling2D(), layers.Flatten(), layers.Dropout(0.2), layers.Dense(128),
                    layers.Dense(len(category))])

model.compile(optimizer="adam", loss=losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
model.fit(data_train, validation_data=data_validation, epochs=25)
model.save("imageClassification.keras")