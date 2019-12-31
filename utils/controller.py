from pynput.keyboard import Key, Controller
from inputs import get_gamepad
import keyboard
import math
import threading
from .directkeys import PressKey, ReleaseKey, W, A, D
from time import sleep
import os
from keras.models import model_from_json
import numpy as np

# https://github.com/kevinhughes27/TensorKart/blob/master/utils.py
class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):

        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()


    def read(self):
        x = self.LeftJoystickX
        rt = self.RightTrigger
        lt = self.LeftTrigger
        '''
        a = self.A
        b = self.X # b=1, x=2
        '''
        return [round(x, 2), round(rt, 2), round(lt, 2)] 


    def _monitor_controller(self):
        while True:
            events = get_key()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state

#Temporal, while i find a solution to vJoy input.
class KeyboardInputs():
    def __init__(self):

        self.a = 0
        self.nothing = 1
        self.d = 0

        self.pause = False
        self.exit = False

        self.monitor_thread = threading.Thread(target=self.monitor, args=())
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def read(self):
        return [self.a, self.nothing, self.d]
    
    def shortcuts(self):
        return self.pause, self.exit

    def monitor(self):
        while True:
            
            if keyboard.is_pressed('a'): 
                self.a = 1
                self.nothing = 0
            elif keyboard.is_pressed('d'):
                self.d = 1
                self.nothing = 0

            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('p'):
                self.pause = not self.pause

            elif keyboard.is_pressed('ctrl') and keyboard.is_pressed('e'):
                self.exit = True

            else:
                self.a = 0
                self.nothing = 1
                self.d = 0


class Car():
    def __init__(self, path):

        models_accuracies = []
        for i, model in enumerate(os.listdir(path)):
            if not model == 'model.json':
                models_accuracies.append([i, float(model[10:18])])
        
        max_accuracy = max(models_accuracies, key=lambda x:x[1])  

        model_name = f"{os.listdir(path)[max_accuracy[0]]}"

        model_json_path = path + 'model.json'
        model_h5_path = path + model_name

        with open(model_json_path, 'r') as json_file:
            loaded_model_json = json_file.read()

        self.model = model_from_json(loaded_model_json)
        self.model.load_weights(model_h5_path)

        self.pause = False

        self.update_thread = threading.Thread(target=self.update, args=())
        self.update_thread.daemon = True
        self.update_thread.start()

    def drive(self, frame, pause):
        self.pause = pause

        prediction = np.argmax(self.model.predict(np.array([frame]))[0])
        
        if not self.pause:
            PressKey(W)

            if prediction == 0:
                if random.randrange(0,3) == 1:
                    PressKey(W)
                else:
                    ReleaseKey(W)
                PressKey(A)
                ReleaseKey(D)

            if prediction == 1:
                PressKey(W)
                ReleaseKey(A)
                ReleaseKey(D)
                print('Nothing')

            if prediction == 2:
                if random.randrange(0,3) == 1:
                    PressKey(W)
                else:
                    ReleaseKey(W)
                PressKey(D)
                ReleaseKey(A)
                ReleaseKey(S)
                print('Right')
            
        else:
            ReleaseKey(W)
            ReleaseKey(D)
            ReleaseKey(A)
    
    def update(self):
        while not self.pause:
            sleep(0.2)
            #ReleaseKey(W)
            ReleaseKey(D)
            ReleaseKey(A)
