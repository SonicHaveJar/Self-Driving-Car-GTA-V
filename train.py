import numpy as np
import pandas as pd
from sklearn.utils import shuffle

from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Lambda, Conv2D, Dropout, Dense, Flatten
from keras.callbacks import ModelCheckpoint
from keras.utils import to_categorical

from PIL import Image
import os

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
        print("jio")

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

model = Sequential()
model.add(Lambda(lambda x: x/127.5-1.0, input_shape=(300, 1100, 3)))
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
model.add(Dense(3, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model_json = model.to_json()
with open("./data/models/model.json", "w") as json_file:
    json_file.write(model_json)

checkpoint = ModelCheckpoint('./data/models/model-{epoch:03d}-{accuracy:03f}-{val_accuracy:03f}.h5', verbose=1, monitor='val_loss', save_best_only=True, mode='auto')  

model.fit(X, y_, batch_size=6, epochs=15, validation_split=0.2, callbacks=[checkpoint], verbose=1)
