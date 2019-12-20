import numpy as np
import cv2
from mss import mss
from PIL import Image

mon = {'top': int((1080/2)-(300/2)), 'left': int((1920/2)-(300/2)), 'width': 300, 'height': 300}

sct = mss()

kernel_size = 5

low_threshold = 100
high_threshold = 150

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 50  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments


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

#https://gist.github.com/pknowledge/86a148c6cd5f0f2820ba81561cc00a8e
def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    channel_count = img.shape[2]
    match_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, vertices, match_mask_color)
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

#https://stackoverflow.com/questions/45322630/how-to-detect-lines-in-opencv
def get_road_lines(view=False):
    sct.get_pixels(mon)

    frame = np.array(Image.frombytes('RGB', (sct.width, sct.height), sct.image))

    region = region_of_interest(frame, np.array([vertices], np.int32))

    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    blur_gray = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

    line_image = np.copy(frame) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)
    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    except:
        pass

    lines_edges = cv2.addWeighted(frame, 0.8, line_image, 1, 0)

    if view:
        cv2.imshow('Lines view', lines_edges)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()

    #return lines_edges