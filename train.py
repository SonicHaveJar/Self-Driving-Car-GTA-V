import numpy as np
import pandas as pd
from sklearn.utils import shuffle

from tensorflow.python.keras import backend as k

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import TensorBoard

from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2

from PIL import Image
import os
import time

path = './data/'
imgs_path = path + 'imgs/'

file = path + 'data.csv'

df = pd.read_csv(file, names=['img', 'left', 'nothing', 'right'])

df['left'][1:] = df['left'][1:].apply(lambda x: int(x))
df['nothing'][1:] = df['nothing'][1:].apply(lambda x: int(x))
df['right'][1:] = df['right'][1:].apply(lambda x: int(x))

left = []
nothing = []
right = []

for data in df.values[1:]:
    img = data[0]
    action = data[1:]
    
    if action[0] == 1:
        left.append([img, [1, 0, 0]])
    elif action[1] == 1:
        nothing.append([img, [0, 1, 0]]) 
    elif action[2] == 1:
        right.append([img, [0, 0, 1]])
    else:
        print("Press F to pay respects.")

counter = [len(left), len(nothing), len(right)]

limit = min(counter)

left = shuffle(left)
nothing = shuffle(nothing)
right = shuffle(right)

left = left[:limit]
nothing = nothing[:limit]
right = right[:limit]

training_data = left + nothing + right
training_data = np.array(shuffle(training_data))

training_df = pd.DataFrame(training_data)

X, y = training_df[0], training_df[1]

X_imgs = []
for img in X.values:
    im = Image.open(img)
    X_imgs.append(np.array(im))
    im.close()

X = np.array(X_imgs)

y_ = np.array([np.array(i) for i in y])

input_shape = (300, 1100, 3)

def nvidia_model():
    model = Sequential()
    model.add(Lambda(lambda x: x/127.5-1.0, input_shape=input_shape))
    model.add(Conv2D(24, 5, 2, activation='elu'))
    model.add(Conv2D(36, 5, 2, activation='elu'))
    model.add(Conv2D(48, 5, 2, activation='elu'))
    model.add(Conv2D(64, 3, activation='elu'))
    model.add(Conv2D(64, 3, activation='elu'))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(100, activation='elu'))
    model.add(Dense(50, activation='elu'))
    model.add(Dense(10, activation='elu'))
    model.add(Dense(3, activation='softmax'))

    return 'nvidia_model', model

def XceptionV1():
    xception_model = Xception(include_top=False, weights='imagenet', input_shape=input_shape)

    x = xception_model.output
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    preds = Dense(3, activation='softmax')

    model = Model(input=xception_model.input, output=preds)

    return 'XceptionV1', model

def Inception_ResNet_V2():
    irv2 = InceptionResNetV2(include_top=False, weights='imagenet', input_shape=input_shape)

    x = irv2.output
    x = Dropout(0.5)(x)
    x = Flatten()(x)
    preds = Dense(3, activation='softmax')

    model = Model(input=irv2.input, output=preds)

    return 'InceptionResNetV2', model

name, model = XceptionV1()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model_json = model.to_json()
with open(f"./data/models/{name}.json", "w") as json_file:
    json_file.write(model_json)

#checkpoint = ModelCheckpoint(f'./data/models/{name}-{epoch:03d}-{accuracy:03f}-{val_accuracy:03f}.h5', verbose=1, monitor='val_loss', save_best_only=True, mode='auto')  
log_dir=r".\data\logs\fit\\" + name
tensorboard = TensorBoard(log_dir=log_dir)

model.fit(X, y_, batch_size=32, epochs=30, validation_split=0.1, callbacks=[tensorboard], verbose=1)