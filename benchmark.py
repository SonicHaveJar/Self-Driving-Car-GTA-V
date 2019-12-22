from utils.controller import KeyboardInputs
from utils.screen import capture, fps
import keyboard
from time import time, sleep
import numpy as np
from sys import argv

#        BENCHMARK IN MY PC
#+---------------------------------+
#|                 |  Average FPS  |
#+---------------------------------+
#| View enabled    | 8.24212239173 |
#| View disabled   | 11.3710106884 |
#+---------------------------------+

arg = int(argv[1])
view = True if arg == 1 else False

k = KeyboardInputs()

fpss = []

script_start = time()
input("Ready to start do a benchmark?, press any key to when you are ready to play some gta.")
print("Waiting 5 seconds...")
sleep(5)
print("Running benchmark...")
while 1:
    last = time()

    k_input = k.read()
    frame = capture(view=view)

    data = [2, *k_input]

    fpss.append(fps(last))

    if int(time()-script_start) == 60:
        break

print(f"Average: {np.mean(fpss)}")