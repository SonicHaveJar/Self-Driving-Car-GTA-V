import numpy as np
import cv2
from mss import mss
from PIL import Image

screen_size = (1920, 1080)
#gta_window_size = (800, 600)
map_size = (157, 100)

top = int((screen_size[1]/2)+197)
left = int((screen_size[0]/2)-392)

mon = {'top': top, 'left': left, 'width': map_size[0], 'height': map_size[1]}

sct = mss()

def capture_map(view=False):
    sct.get_pixels(mon)

    frame = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
    
    #Read this for an explanation https://stackoverflow.com/a/48367205
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(135, 100, 20), (165, 255, 255))

    if view:
        cv2.imshow('map', mask)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    mask_3d = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    resized_mask = np.array(cv2.resize(mask_3d, (300, 300), interpolation=cv2.INTER_AREA))
    return resized_mask