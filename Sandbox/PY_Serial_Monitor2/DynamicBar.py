from tkinter import *

class DynamicBar(Canvas):

    def __init__(self, root, width, height, data_start, data_end, *args, **kw):
        super(DynamicBar, self).__init__(root, width=width, height=height, *args, **kw)
        self.width = width
        self.height = height
        self.data_start = data_start
        self.data_end = data_end
        bg = self.create_rectangle(0, 0, width, height)
        self.bar = self.create_rectangle(0, height, width, 2 * height, fill="red")

    def set_data(self, data):
        pos = self.coords(self.bar)
        newy = self.height - (data - self.data_start) / (self.data_end - self.data_start) * self.height
        diff = newy - pos[1]
        self.move(self.bar, 0, diff)

    