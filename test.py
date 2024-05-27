from keras import layers, utils, Sequential, losses, models
import matplotlib as plt
import tensorflow as tf
import pandas as pd
import numpy as np
import commands

validation_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Objects\\Validation"
train_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Objects\\Train"
test_path = "C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\imageClassificationFolder\\Objects\\Test"

image_width = 165
image_height = 165

data_train = utils.image_dataset_from_directory(train_path, shuffle=True, image_size=(image_width, image_height), batch_size=32, validation_split=False)
category = data_train.class_names

# v Pegando e adaptando as imagens como database do Keras
data_validation = utils.image_dataset_from_directory(validation_path, shuffle=False, image_size=(image_width, image_height), batch_size=32, validation_split=False)
data_test = utils.image_dataset_from_directory(test_path, shuffle=False, image_size=(image_width, image_height), batch_size=32, validation_split=False)

                        # v Ajuste de cores                 # 1º Filtros 2º RGB 4º Ativação padrão para datasets medianos
model = Sequential([layers.Rescaling(1./255), layers.Conv2D(16, 3, padding='same', activation='relu'), 
                    layers.MaxPooling2D(), layers.Conv2D(32, 3, padding='same', activation='relu'),
                    layers.MaxPooling2D(), layers.Conv2D(64, 3, padding='same', activation='relu'),
                    layers.MaxPooling2D(), layers.Flatten(), layers.Dropout(0.2), layers.Dense(128),
                    layers.Dense(len(category))])

# 1º Para operação com grandes informações
model.compile(optimizer="adam", loss=losses.SparseCategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
model.fit(data_train, validation_data=data_validation, epochs=15)
model.save("Machine_Learning\\imageClassificationFolder\\imageClassification.keras")

print(model.history.history['val_accuracy'])
print(model.history.history['val_loss'])

'''
model = models.load_model("Machine_Learning\\imageClassification.keras")
image = utils.load_img("images.jpg", target_size=(image_height, image_width))
array = utils.array_to_img(image)
imgBat = tf.expand_dims(array, 0)

preditcion = model.predict(imgBat)
print(commands.fruitNVegetablesNames[np.argmax(preditcion)])
'''