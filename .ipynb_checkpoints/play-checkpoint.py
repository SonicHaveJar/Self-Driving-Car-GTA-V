import numpy as np

from utils.controller import KeyboardSimulator
from utils.screen import capture

from time import sleep

from keras.models import model_from_json

simulator = KeyboardSimulator()

model_path = "./data/models/"

model_json_path = model_path + 'model.json'
model_h5_path = model_path + 'model-001-0.331644-0.337690.h5'

# load json and create model
with open(model_json_path, 'r') as json_file:
    loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights(model_h5_path)
print(f"Loaded {model_path}")

print("Waiting 5 seconds...")
sleep(5)
print("Running...")
while 1:
    frame = capture()

    prediction = int(np.rint(model.predict(np.array([frame])))[0][0])

    simulator.steering(prediction)

    print(prediction)