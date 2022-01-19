from tkinter import *
import time
import random
from PreloadDisplay import PreloadDisplay
from global_funcs import *
from framework import framework
import matplotlib.pyplot as plt
from SuccessRecordDisplay import SuccessRecordDisplay

def show_app(port, pat_id, sess):
    root = Tk()
    root.configure(bg="white")

    preload_max = 0.47
    preload_min = 0.45
    frame = None

    def on_closing():
        frame.exit()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    label = Label(root, text=port + " " + str(pat_id) + " " + str(sess))
    label.configure(bg="white")
    label.grid(row=0, column=0)

    global success_count
    global failure_count
    success_count = 0
    failure_count = 0

    global success_record
    success_record = []

    def update_successes():
        global success_count
        global failure_count
        global success_lbl
        global failure_lbl
        success_count = 0
        failure_count = 0
        for record in success_record:
            if record:
                success_count += 1
            else:
                failure_count += 1
        # success_lbl.configure(text="Successes: " + str(success_count))
        # failure_lbl.configure(text="Failures: " + str(failure_count))

    def update_torque():
        global torque_lbl
        torque_lbl.configure(text="Torque: " + format(torque_value, ".4f"))

    def on_start():
        global success_record
        if random.random() < 0.5:
            success_record.append(True)
        else:
            success_record.append(False)
        update_successes()

    def on_pause():

        if frame.running:
            frame.stop()
        else:
            frame.start()

    def trash_prev():
        global success_record
        success_record = success_record[0:-1]
        update_successes()

    big_w = 11
    big_h = 4
    start_btn = Button(root, text="Start", command=on_start, width=big_w, height=big_h,
                       bg="green", font=button_font, fg=button_font_color)
    start_btn.grid(row=4, column=0, padx=padx, pady=pady)

    pause_btn_color_swap = True
    swap_time = 0
    PAUSE_BLINK_RATE = .5
    pause_btn = Button(root, text="Pause", command=on_pause, width=big_w, height=big_h,
                       bg="red", font=button_font, fg=button_font_color)
    pause_btn.grid(row=4, column=1, padx=padx, pady=pady)

    trash_btn = Button(root, text="Trash Prev\nResult", command=trash_prev, width=big_w, height=big_h,
                       bg="blue", font=button_font, fg=button_font_color)
    trash_btn.grid(row=4, column=2, padx=padx, pady=pady)

    global success_lbl
    global failure_lbl
    global torque_lbl
    success_lbl = Label(root)
    success_lbl.configure(bg="white")
    success_lbl.grid(row=3, column=0)
    failure_lbl = Label(root)
    failure_lbl.configure(bg="white")
    failure_lbl.grid(row=3, column=1)
    torque_lbl = Label(root)
    torque_lbl.configure(bg="white")
    torque_lbl.grid(row=3, column=2)
    update_successes()

    preload_display = PreloadDisplay(root, 200, 400, preload_min, preload_max)
    preload_display.grid(row=4, column=0)
    preload_display.configure(bg="white")

    nw = 15
    nh = 5
    i = 0
    display = SuccessRecordDisplay(
        root, 600, 200, nw, nh, margin=15, radius=15)
    display.grid(row=4, column=4)


    root.geometry("1200x600")
    center_window(root)
    torque_value = 0

    frame = framework(port, patID=pat_id, sess=sess,
                      premin=preload_min, premax=preload_max, no_motor=False, no_emg=False)

    while 1:
        if frame.mot:
            if frame.mot.torque_update:
                torque_value = frame.mot.torque_value
                frame.mot.torque_update = False
                update_torque()
                preload_display.update_data(torque_value)

        if not frame.running:

            if pause_btn_color_swap and time.time() - swap_time > PAUSE_BLINK_RATE:
                pause_btn_color_swap = not pause_btn_color_swap
                pause_btn.configure(bg="red")
                swap_time = time.time()

            elif not pause_btn_color_swap and time.time() - swap_time > PAUSE_BLINK_RATE:
                pause_btn_color_swap = not pause_btn_color_swap
                pause_btn.configure(bg="green")
                swap_time = time.time()
        else:
            pause_btn.configure(bg="red")

        if frame.show_emg:
            display.set_record(i, random.randint(0, 1))
            i += 1
            if i == nw * nh:
                i = 0
                display.reset_all()
            frame.show_emg = False
            yemg = frame.current_trial.emg_data[-400:]
            yacc = [sample / 3.0 for sample in frame.current_trial.acc_data[-400:]]
            
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            ax.clear()

            ax.plot( yemg, 'r', label="EMG")
            ax.plot( yacc, label="acc")

            # Format plot
            plt.title('EMG Readings')
            plt.ion()
            plt.legend()
            plt.show()
            plt.pause(5)
            plt.close()
           
        center_window(root)
        root.update()


if __name__ == "__main__":
    show_app("COM15", 1234, 1)
