from tkinter import *

from matplotlib.pyplot import fill
from DynamicBar import *
import serial
from threading import Thread
import numpy as np
import time

def receiving(ser):
    global last_received
    global rolling_avg

    buffer_string = ''
    while True:
        # print("a")
        try:
            buffer_string = buffer_string + ser.read(ser.inWaiting()).decode()
        except UnicodeDecodeError:
            continue
        if '\n' in buffer_string:
            # Guaranteed to have at least 2 entries
            lines = buffer_string.split('\n')
            last_received = lines[-2]
            # If the Arduino sends lots of empty lines, you'll lose the
            # last filled line, so you could make the above statement conditional
            # like so: if lines[-2]: last_received = lines[-2]
            rolling_avg.append(clean_adc(last_received)[0])
            rolling_avg.pop(0)
            buffer_string = lines[-1]



def clean_adc(input):
    try:
        reading = input.strip('\r\n').split(',')
        if len(reading) == 2:
            return [float(x) for x in reading]
        else:
            raise ValueError()
    except (UnicodeDecodeError, ValueError) as e:
        return [0.0, 0.0]


try:
    root = Tk()

    width = 200
    height = 500
    canvas = DynamicBar(root, width=width, height=height, data_start=0, data_end=3412-2148)
    # Max voltage = 3412
    # DC Offset = 2148
    canvas.pack()


    last_received = "Here we go"
    num_samples = 30
    rolling_avg = [0 for _ in range(num_samples)]
    # Initialize communication with Serial
    COM = 'COM3'  # /dev/ttyACM0 (Linux)
    BAUD = 500000
    ser = serial.Serial(COM, BAUD, timeout=.1)

    thread = Thread(target=receiving, args=(ser,), daemon=False)
    thread.start()
    while True:
        data = np.mean(np.abs(rolling_avg - np.full(shape=num_samples, fill_value=2149)))
        # data = np.mean(rolling_avg)
        # print(data)
        canvas.set_data(data)
        root.update()
finally:
    ser.close()