from pyvjoy import VJoyDevice
from time import sleep
import random

class XboxControllerSimulator():
    def __init__(self):
        self.vjoy = VJoyDevice(1)

        self.MAX_VJOY = 32767

        self.vjoy.reset()

    def steering(self, value):
        self.vjoy.data.wAxisX = int(value * self.MAX_VJOY)
        self.vjoy.data.wAxisY = int(0.5 * self.MAX_VJOY)
        self.vjoy.update()

simulate = XboxControllerSimulator()
while 1:
    c = random.randrange(-10, 10)/10

    print(c)
    sleep(0.2)
    simulate.steering(c)
    '''
    


    #The 'efficient' method as described in vJoy's docs - set multiple values at once

    j.data


    j.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
    j.data.wAxisX = 0x2000 
    j.data.wAxisY= 0x7500

    #send data to vJoy device
    j.update()
    '''
