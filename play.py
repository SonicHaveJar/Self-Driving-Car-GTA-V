import numpy as np
from utils.controller import Agent
from utils.screen import capture
from time import sleep

agent = Agent('./data/models/')

print("Waiting 5 seconds...")
sleep(5)
print("Running...")
while 1:
    frame = capture()

    agent.drive(frame)
