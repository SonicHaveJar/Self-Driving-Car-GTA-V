import numpy as np
import cv2
from mss import mss
from PIL import Image

#https://stackoverflow.com/a/43560140
mon = {'top': int((1080/2)-(300/2)), 'left': int((1920/2)-(300/2)), 'width': 300, 'height': 300}

sct = mss()

def capture(view=False):
    sct.get_pixels(mon)

    frame = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))
    frame_rgb = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if view:
        cv2.imshow('Game view', frame_rgb)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    return frame_rgb