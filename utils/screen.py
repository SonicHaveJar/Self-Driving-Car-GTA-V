import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
from .map import capture_map

#        BENCHMARK IN MY PC
#+---------------------------------+
#|                 |  Average FPS  |
#+---------------------------------+
#| View enabled    | 8.24212239173 |
#| View disabled   | 11.3710106884 |
#+---------------------------------+

screen_size = (1920, 1080)
#gta_window_size = (800, 600)
capture_size = (800, 300)

top = int((screen_size[1]/2)-(capture_size[1]/2))
left = int((screen_size[0]/2)-(capture_size[0]/2))

#https://stackoverflow.com/a/43560140
mon = {'top': top, 'left': left, 'width': capture_size[0], 'height': capture_size[1]}

sct = mss()

def capture(view=False):
    sct.get_pixels(mon)

    frame = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
    frame_rgb = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    full_observation = np.concatenate((capture_map(), frame_rgb), axis=1)

    if view:
        cv2.imshow('Game view', full_observation)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    return full_observation

def fps(last_time):
    time_elapsed =  time() - last_time

    fps = 1/time_elapsed

    return fps
    #print(f"FPS: {fps}")
    