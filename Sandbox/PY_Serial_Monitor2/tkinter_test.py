from tkinter import *
import random
import time
import numpy as np

from DynamicBar import DynamicBar

root = Tk()

width = 200
height = 500
canvas = DynamicBar(root, width=width, height=height, data_start=100, data_end=200)
canvas.pack()

data = 150

random_speed = 15
speed = 1
canvas.set_data(data)



while True:
    canvas.set_data(data)
    # data += random_speed * random.random() - random_speed / 2
    data += speed
    if data < 100 or data >= 200:
        speed = -speed
    root.update()