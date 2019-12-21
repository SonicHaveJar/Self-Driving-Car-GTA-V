#PyTorch version soon.
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from keras.callbacks import ModelCheckpoint

from PIL import Image
import os

path = './data/'
imgs_path = path + 'imgs/'

file = path + 'data.csv'

df = pd.read_csv(file, names=['img', 'steering'])

X = df['img'][1:]
y = df['steering'][1:]

X = [np.array(Image.open(img)) for img in X.values]

X = np.array(X)

model = Sequential()
model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(300, 300, 3)))
model.add(Conv2D(24, 5, 5, activation='elu', subsample=(2, 2)))
model.add(Conv2D(36, 5, 5, activation='elu', subsample=(2, 2)))
model.add(Conv2D(48, 5, 5, activation='elu', subsample=(2, 2)))
model.add(Conv2D(64, 3, 3, activation='elu'))
model.add(Conv2D(64, 3, 3, activation='elu'))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(100, activation='elu'))
model.add(Dense(50, activation='elu'))
model.add(Dense(10, activation='elu'))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

checkpoint = ModelCheckpoint('./data/models/model-{epoch:03d}-{accuracy:03f}-{val_accuracy:03f}.h5', verbose=1, monitor='val_loss', save_best_only=True, mode='auto')  

model.fit(X, y, batch_size=16, epochs=1, validation_split=0.2, callbacks=[checkpoint], verbose=1)
