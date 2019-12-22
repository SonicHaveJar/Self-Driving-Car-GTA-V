from utils.controller import XboxController, KeyboardInputs
from utils.screen import capture, fps
import cv2
import csv
import os
from time import sleep, time
import numpy as np
from sys import argv

#        BENCHMARK IN MY PC
#+---------------------------------+
#|                 |  Average FPS  |
#+---------------------------------+
#| View enabled    | 8.24212239173 |
#| View disabled   | 11.3710106884 |
#+---------------------------------+

view_arg = int(argv[1])
fps_arg = int(argv[2])

view = True if view_arg == 1 else False
fps_show = True if fps_arg == 1 else False

#ctrl = XboxController()
k = KeyboardInputs()

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
    #writer.writerow(['img', 'steering'])
    writer.writerow(['img', 'left', 'nothing', 'right'])
else:
    csv_file = open(file, 'a')
    writer = csv.writer(csv_file)

print("Waiting 5 seconds...")
sleep(5)
i = 0
#add hotkeys
print("Running...")
while 1:
    if fps_show:
        last = time()
    #ctrl_input = ctrl.read()
    k_input = k.read()
    frame = capture(view=True)
    
    frame_path = f"{imgs_path}{i}.jpg"
    cv2.imwrite(frame_path, frame)

    data = [frame_path, *k_input]

    writer.writerow(data)

    if fps_show:
        print(fps(last))

    i+=1
csv_file.close()