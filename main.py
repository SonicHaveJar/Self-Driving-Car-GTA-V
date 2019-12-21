from utils.controller import XboxController
from utils.screen import capture
import cv2
import csv
import os
from time import sleep
import numpy as np

ctrl = XboxController()

path = './data/'
imgs_path = path + 'imgs/'

models_path = path + 'models/'

file = path + 'data.csv'

if not os.path.exists(path):
    os.makedirs(path)
    os.makedirs(imgs_path)
    os.makedirs(models_path)

elif not os.path.exists(imgs_path):
    os.makedirs(imgs_path)

elif not os.path.exists(models_path):
    os.makedirs(models_path)

if not os.path.exists(file):
    csv_file = open(file, 'a')
    writer = csv.writer(csv_file)
    writer.writerow(['img', 'steering'])
else:
    csv_file = open(file, 'a')
    writer = csv.writer(csv_file)

print("Waiting 5 seconds...")
sleep(5)
i = 0
print("Running...")
while 1:
    ctrl_input = ctrl.read()
    frame = capture()
    
    frame_path = f"{imgs_path}{i}.jpg"
    cv2.imwrite(frame_path, frame)

    data = [frame_path, ctrl_input[0]]

    writer.writerow(data)

    i+=1
csv_file.close()