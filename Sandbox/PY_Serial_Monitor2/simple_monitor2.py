from tkinter import *

from matplotlib.pyplot import fill
from numpy.testing._private.utils import measure
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

# can be "normal" or "rectified"
read_mode = "rectified"

def get_reading():
    global rolling_avg
    global num_samples
    if read_mode == "rectified":
        return np.mean(np.abs(rolling_avg - np.full(shape=num_samples, fill_value=2149)))
    elif read_mode == "normal":
        return np.mean(rolling_avg)

try:
    root = Tk()

    width = 200
    height = 500
    canvas = DynamicBar(root, width=width, height=height, data_start=0, data_end=3412-2148 if read_mode == "rectified" else 3412)
    # Max voltage = 3412
    # DC Offset = 2148
    canvas.pack()

    MVC_time = 4    # seconds
    toggle_MVC_enabled = False
    def on_MVC_click():
        global toggle_MVC_enabled
        def fun():
            global toggle_MVC_enabled
            toggle_MVC_enabled = True
            readings = []
            start = time.time()
            while time.time() < start + MVC_time:
                readings.append(get_reading())
            canvas.data_end = np.mean(readings)
            print(canvas.data_end)
            toggle_MVC_enabled = True
        Thread(target=fun, daemon=False).start()
    measure_MVC = Button(text="Measure MVC", command=on_MVC_click)
    measure_MVC.pack()


    last_received = "Here we go"
    num_samples = 60
    rolling_avg = [0 for _ in range(num_samples)]
    # Initialize communication with Serial
    COM = 'COM15'  # /dev/ttyACM0 (Linux)
    BAUD = 500000
    ser = serial.Serial(COM, BAUD, timeout=.1)

    thread = Thread(target=receiving, args=(ser,), daemon=False)
    thread.start()
    while True:
        if toggle_MVC_enabled:
            measure_MVC["state"] = "normal" if measure_MVC["state"] == "disabled" else "disabled"
            toggle_MVC_enabled = False
        data = get_reading()
        # data = np.mean(rolling_avg)
        # print(data)
        canvas.set_data(data)
        root.update()
finally:
    ser.close()