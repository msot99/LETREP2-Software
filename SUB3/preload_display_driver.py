from tkinter import *
import time
import random
from PreloadDisplay import PreloadDisplay
from global_funcs import *
import math


if __name__ == "__main__":
    root = Tk()
    pd = PreloadDisplay(root, 220, 300, 1, 0)
    pd.pack()

    f = 0.5
    w = 2 * math.pi * f
    t = 0
    dt = 0.01

    while 1:
        data = math.sqrt(2) * math.sin(w * t)
        pd.update_data(data)
        print(data)
        time.sleep(dt)
        t += dt
        root.update()