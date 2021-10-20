

from time import sleep
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from emg import emg
from statistics import mean
from itertools import chain

def animate(i, xs, ys):

    # Limit x and y lists to 20 items
    
    ys = ys[-5000:]
    # n = 20
    # list1 = [sum(ys[i:i+n])/n for i in range(0,len(ys),n)]

    
    xs = xs[-1*len(ys):]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.title('EMG Readings')
    plt.ylim([0, 6])


last_received = "Here we go"

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [i for i in range(0, 5001)]
ys = [i for i in range(0, 200)]

emg_obj = emg(ys)
emg_obj.Connect()
emg_obj.Scan()
emg_obj.Start()

try:
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
    plt.show()
finally:
    emg_obj.Stop()
    print("Good Exit")
