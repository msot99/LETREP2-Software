from tkinter import *

class PreloadDisplay(Canvas):

    def __init__(self, root, width, height, max, min, *args, **kw):
        super(PreloadDisplay, self).__init__(root, width=width, height=height, *args, **kw)
        self.width = width
        self.height = height
        self.preload_max = max
        self.preload_min = min
        self.high_image = PhotoImage(file='HighImage.png')
        self.low_image  = PhotoImage(file='LowImage.png')
        self.good_image = PhotoImage(file='GoodImage.png')
        self.high = self.create_image(0, 0, image=self.high_image)
        self.low  = self.create_image(200, 100, image=self.low_image)
        self.good = self.create_image(200, 100, image=self.good_image)
        self.update_data((max + min) / 2)

    def update_data(self, torque):
        y = (torque - self.preload_min) / (self.preload_max - self.preload_min)
        if y > 1:
            pass
        elif y < 1:
            pass
        else:
            pass