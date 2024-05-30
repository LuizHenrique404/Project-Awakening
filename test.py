import tensorflow as tf
import pandas as pd
from os import path
import numpy as np

S = 'synthetic_datasets'
M = 'MNIST'
I = 'images'

train_df = pd.read_csv(path.join(S, M, 'training_data.csv'), header=None)
columns = ['path', 'class_index', 'xmin', 'ymin', 'xmax', 'ymax']

train_df.columns = columns

test_df = pd.read_csv(path.join(S, M, 'test_data.csv'), header=None)
test_df.columns = columns

t = 'MNIST_Converted_Training'
train_df['path'] = train_df['path'].apply(lambda s: path.join(S, M, I, t, s))

t = 'MNIST_Converted_Testing'
test_df['path'] = test_df['path'].apply(lambda s: path.join(S, M, I, t, s))

row1 = train_df.iloc[0].to_numpy().tolist()