from utils.controller import XboxController
from utils.record_window import capture
import cv2
import csv
import os
from time import sleep

ctrl = XboxController()

path = r'C:\Users\javie\Desktop\GTA V Self Driving Car/data/'
imgs_path = path + 'imgs/'

file = path + 'data.csv'

if not os.path.exists(path):
    os.makedirs(path)
    os.makedirs(imgs_path)

elif not os.path.exists(imgs_path):
    os.makedirs(imgs_path)

if not os.path.exists(file):
    csv_file = open(file, 'a')
    writer = csv.writer(csv_file)
    writer.writerow(['img', 'steering','throttle', 'brake'])
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

    one_hot_vector = [frame_path, ctrl_input[0], ctrl_input[1], ctrl_input[2]]

    writer.writerow(one_hot_vector)

    #print(ctrl_input, i)
    i+=1
print(f"Stopped, saves at {path}.")

csv_file.close()
