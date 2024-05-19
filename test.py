# https://pyimagesearch.com/start-here/

from keras import datasets, layers, models
import matplotlib.pyplot as plt
from tensorflow import keras
import numpy as np
import cv2

# Receber e Adaptar as informações.
(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images / 255, testing_images / 255

class_names = ["Plane", "Car", "Bird", "Deer", "Dog", "Frog", "Horse", "Ship", "Truck"]

# Redução das imagens para treino.
training_images = training_images[:20000]
training_labels = training_labels[:20000]
testing_images = testing_images[:4000]
testing_labels = testing_labels[:4000]
# Para tornar o procedimento mais rápido (Disconta a precisão)

# As camadas para operações da rede neural serão ativadas de maneira sequencial
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (2, 2), activation="relu"))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (2, 2), activation="relu"))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation="relu"))
model.add(layers.Dense(10, activation="softmax"))
# A ultima basicamente servirá para poder entregar uma probabilidade de acerto.

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
# epochs - Significa quantas vezes o sistema testará com a mesma imagem (Default = 1)

loss, accuracy = model.evaluate(testing_images, testing_labels)
print(f"Loss: {loss} \nAccuracy: {accuracy}")

# Irá salvar o modelo em um arquivo que poderá ser carregado para evitar a repetição do treino.
model.save("image_classifier.keras")
# models.load_model("arquivo.keras")