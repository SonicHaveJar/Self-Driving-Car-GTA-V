import numpy as np
import cv2
from mss import mss
from PIL import Image

mon = {'top': int((1080/2)-(300/2)), 'left': int((1920/2)-(300/2)), 'width': 300, 'height': 300}

sct = mss()

height = mon['height']
width = mon['width']

separation = 70
altura = 160
center_altura = 100
vertices = [
    (0, height),
    (0, height-altura),
    (width/2 -separation/2, center_altura),
    (width/2+separation/2, center_altura),
    (width, height-altura),
    (width, height)
]


def roi(frame, vertices):
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(frame, mask)
    return masked

def black_and_white(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = 200
    frame = cv2.threshold(frame, thresh, 255, cv2.THRESH_BINARY)[1]
    return frame

# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html for more information
def get_road_lines(view=False):
    sct.get_pixels(mon)

    frame = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))

    region = roi(frame, np.array([vertices], np.int32))

    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray ,50, 150,apertureSize=3)

    cv2.imshow('edges', edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow('image', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()

    #gray = cv2.cvtColor(region,cv2.COLOR_BGR2GRAY)

    #blurred = cv2.GaussianBlur(gray, (11, 11), 0)

    #edged = cv2.Canny(blurred, 30, 150)

    #lines = cv2.HoughLines(edged, 1, np.pi / 180, 25)
