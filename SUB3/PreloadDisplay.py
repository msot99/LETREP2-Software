from tkinter import *
from PIL import Image, ImageTk
import math

# animation constants
dx = 7
dy = 70
r = 0.5 * (dy**2 / dx - dx)
thetamax = math.asin(dy / r)
a = 1
image_width = 200
image_height = 100

class PreloadDisplay(Canvas):



    def __init__(self, root, width, height, max, min, *args, **kw):
        super(PreloadDisplay, self).__init__(root, width=width, height=height, *args, **kw)
        self.width = width
        self.height = height
        self.preload_max = max
        self.preload_min = min

        self._bg = self.create_rectangle(0, 0, width, height, fill="#0ed145")
        self.high_image = Image.open('HighImage.png')
        self.low_image  = Image.open('LowImage.png')
        self.good_image = Image.open('GoodImage.png')
        self._high = self.create_image(100, 50, image=ImageTk.PhotoImage(self.high_image))
        self._low  = self.create_image(100, 50, image=ImageTk.PhotoImage(self.low_image))
        self._good = self.create_image(100, 50, image=ImageTk.PhotoImage(self.good_image))

        self._high_placeholder = None
        self._low_placeholder = None
        self._good_placeholder = None
        self.update_data((max + min) / 2)

    def update_position(self, id, theta, image):
        x = r * (1 - math.cos(theta))
        w = image_width - 2 * x
        y = image_height / 2 - r * math.sin(theta)
        h = image_height / image_width * w
        self.coords(id, self.width / 2, y + self.height / 2 - image_height / 2)
        image = ImageTk.PhotoImage(image.resize((int(w), int(h)), Image.ANTIALIAS))
        self.itemconfigure(id, image=image)
        return image


    def update_data(self, torque):
        z = (torque - self.preload_min) / (self.preload_max - self.preload_min)
        theta = -thetamax * math.atan(a * z)
        self._high_placeholder = self.update_position(self._high, theta + thetamax, self.high_image)
        self._low_placeholder  = self.update_position(self._good, theta, self.good_image)
        self._good_placeholder = self.update_position(self._low,  theta - thetamax, self.low_image)

        if z > 1:
            self.tag_raise(self._high)
            self.itemconfigure(self._bg, fill="#ec1c24")
        elif z < 0:
            self.tag_raise(self._low)
            self.itemconfigure(self._bg, fill="#fff200")
        else:
            self.tag_raise(self._good)
            self.itemconfigure(self._bg, fill="#0ed145")