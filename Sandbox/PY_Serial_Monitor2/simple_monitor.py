
from numpy.core.numeric import roll
import serial
from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from threading import Thread


def receiving(ser):
    global last_received

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


def animate(i, xs, ys):

    # while(rl.s.in_waiting > 0):
    reading = clean_adc(last_received)
    # print(reading)

    # xs.append(reading[1])
    ys.append(reading[0])

    # Limit x and y lists to 20 items
    xs = xs[-50:]
    ys = ys[-50:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.title('ADC Readings')
    plt.ylim([0, 3420])


last_received = "Here we go"
# Initialize communication with Serial
COM = 'COM15'  # /dev/ttyACM0 (Linux)
BAUD = 500000
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [i for i in range(0, 200)]
ys = [i for i in range(0, 200)]
ser = serial.Serial(COM, BAUD, timeout=.1)

Thread(target=receiving, args=(ser,)).start()
try:
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
    plt.show()
finally:
    ser.close()
    print("Good Exit")
