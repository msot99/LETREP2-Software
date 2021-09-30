from tkinter import *
import random
import time

root = Tk()

width = 200
height = 500
canvas = Canvas(root, width=width, height=height)
canvas.pack()

bg = canvas.create_rectangle(0, 0, width, height, fill="light gray")
bar = canvas.create_rectangle(0, 0, width, height, fill="red")

def set_data(data):
    pos = canvas.coords(bar)
    diff = data - pos[1]
    canvas.move(bar, 0, diff)

data = height / 2

random_speed = 15
speed = 4

while True:
    time.sleep(0.01)
    set_data(data)
    # data += random_speed * random.random() - random_speed / 2
    data += speed
    if data < 0 or data >= height:
        speed = -speed
    root.update()