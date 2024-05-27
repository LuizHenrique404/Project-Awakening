# Área para as operações lógicas externas.
'''
SISTEMA DE PONTOS DO USUÁRIO:
-DUAS CASAS DECIMAIS: Pontuação é definida automaticamente para zero. (0.01 > 0.0)
-NÚMERO ACIMA DE DEZ: Todos os pontos são multiplicados por 0.1 (10.0 > 1.0 / 5.0 > 0.5) 
'''

# INCLUIR: Object Detection
# INCLUIR: Image Classification [Feito]
# AO CRIAR SEU PRÓRIO BANCO DE DADOS: Utilize para treinamento ao menos 100 imagens.

from sklearn.model_selection import train_test_split
from keras import utils, models
import tensorflow as tf
import pandas as pd
import numpy as np
import commands

class HumorClassification():
    from sklearn.ensemble import RandomForestClassifier
    
    train_test_results = list()
    model = RandomForestClassifier(n_estimators=60)

    def __init__(self):
        arquive = pd.read_csv("C:\\Users\\Mrleonard\\Documents\\Programs\\Project_Awakening\\Machine_Learning\\humor.csv")
        Y = arquive.drop(columns=["bom","comico","ruim"])
        X = arquive.drop(["resultado"], axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)
        self.train_test_results = [X_train, X_test, y_train, y_test]

        self.model.fit(X_train, y_train.values.ravel())
        print("[SYSTEM] Score Test: ", self.model.score(X_test, y_test))

    def getHumor(self, pontos: dict):
        return self.model.predict([pontos])[0]
    
def imageClassification():    
    image_width = 165
    image_height = 165

    model = models.load_model("Machine_Learning\\imageClassificationFolder\\imageClassification.keras")
    image = utils.load_img("Machine_Learning\\classificationImage.png", target_size=(image_height, image_width))
    array = utils.array_to_img(image)
    imgBat = tf.expand_dims(array, 0)

    preditcion = model.predict(imgBat)
    return commands.objectDetectionNames[np.argmax(preditcion)]