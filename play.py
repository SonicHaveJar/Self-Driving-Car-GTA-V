import numpy as np
from utils.controller import KeyboardInputs, Car
from utils.screen import capture
from time import sleep

keyboard = KeyboardInputs()

car = Car('./data/models/')

print("Waiting 5 seconds...")
sleep(5)
print("Running...")
while 1:
    pause, exit_ = keyboard.shortcuts()

    print(pause)

    if not pause:
        frame = capture()

        car.drive(frame, pause)
    else:
        pass#print("Paused")

    if exit_:
        break
    