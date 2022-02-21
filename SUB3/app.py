from tkinter import *
import time
import random

from cv2 import threshold
from M1Display import M1Display
from PreloadDisplay import PreloadDisplay
from global_funcs import *
from more_options import *
from framework import framework
import matplotlib.pyplot as plt
from SuccessRecordDisplay import SuccessRecordDisplay
from PIL import ImageTk, Image

def show_app(port, pat_id, sess, no_motor=False, no_emg=False):
    root = Tk()
    root.configure(bg="white")
    root.running = True

    options = Options(port, pat_id, sess)

    preload_max = 0.47
    preload_min = 0.45
    frame = None

    def on_closing():
        root.running = False
        root.destroy()
        frame.exit()
    root.protocol("WM_DELETE_WINDOW", on_closing)

    img = Image.open(logo_dir)
    img = img.resize((100, 100), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(img)
    logo_label = Label(root, image=logo, bg="white")
    logo_label.grid(row=0, column=0, padx=padx, pady=pady)

    patient_info_lbl = Label(root, text=str(options.port) + " " + str(options.pat_id) + " " + str(options.sess))
    patient_info_lbl.configure(bg="white")
    patient_info_lbl.grid(row=0, column=1)

    # Start, Pause, Trash, Stop, and Other button functions
    def on_start():
        pass

    def on_pause():
        frame.pause()

    def trash_prev():
        pass
    
    def on_other_options():
        show_more_options(options)

    def on_stop():
        frame.stop()
        general_info_lbl.configure(text="Stopped")
        general_info_lbl.last_updated = time.time()
        

    # Button configuration
    big_w = 11
    big_h = 3

    # start_btn
    start_btn = Button(root, text="Start", command=on_start, width=big_w, height=big_h,
                       bg="green", font=button_font, fg=button_font_color)
    start_btn.grid(row=1, column=0, padx=padx, pady=pady)

    # pause_btn
    pause_btn_color_swap = True
    swap_time = 0
    PAUSE_BLINK_RATE = .5
    pause_btn = Button(root, text="Pause", command=on_pause, width=big_w, height=big_h,
                       bg="red", font=button_font, fg=button_font_color)
    pause_btn.grid(row=2, column=0, padx=padx, pady=pady)

    # trash_btn
    trash_btn = Button(root, text="Trash Prev\nResult", command=trash_prev, width=big_w, height=big_h,
                       bg="blue", font=button_font, fg=button_font_color)
    trash_btn.grid(row=3, column=0, padx=padx, pady=pady)

    # stop_btn
    stop_btn = Button(root, text="Stop", command=on_stop, width=big_w, height=big_h,
                        bg="gray", font=button_font, fg=button_font_color)
    stop_btn.grid(row=0, column=2)

    # other_opts_btn
    other_opts_btn = Button(root, text="More Options", command=on_other_options, width=big_w, height=big_h,
                        bg="gray", font=button_font, fg=button_font_color)
    other_opts_btn.grid(row=0, column=3)


    # Display Frame: widget to hold preload and record displays
    # display_frame
    df_bg = "gray"
    display_frame = Frame(root, bg=df_bg, padx=padx, pady=pady)

    df_title = Label(display_frame, text="Current Trial", bg=df_bg, font=small_font)
    df_title.grid(row=0, column=0)
    df_failure_lbl = Label(display_frame, text="Failure Reason!!", bg=df_bg, font=small_font, fg="red")
    df_failure_lbl.grid(row=1, column=0, columnspan=3)

    nw = 15
    nh = 5
    i = 0
    success_display = SuccessRecordDisplay(
        display_frame, 600, 220, nw, nh, margin=15, radius=15)
    success_display.grid(row=2, column=0, rowspan=2, columnspan=3)
    success_display.configure(bg=df_bg)

    preload_lbl = Label(display_frame, text="Preload Status", bg=df_bg, font=small_font)
    preload_lbl.grid(row=2, column=3)

    preload_display = PreloadDisplay(display_frame, 100, 200, preload_min, preload_max, bg=df_bg)
    preload_display.grid(row=3, column=3)

    m1threshold = 1.3
    m1display = M1Display(display_frame, 100, 200, max=2, min=0, threshold=m1threshold, baseline=1.5, bg=df_bg)

    def show_preload_display():
        m1display.grid_forget()
        preload_display.grid(row=3, column=3)
        preload_lbl.configure(text="Preload Status")
    
    def show_m1display(position):
        preload_display.grid_forget()
        m1display.grid(row=3, column=3)
        preload_lbl.configure(text="M1 Size")
        m1display.update_position(position)

    GI_CLEAR_TIME = 3
    general_info_lbl = Label(display_frame, text="", bg=df_bg, font=large_font)
    general_info_lbl.grid(row=4, column=0, columnspan=4)
    general_info_lbl.last_updated = time.time()

    display_frame.grid(row=1, column=1, rowspan=3, columnspan=3)


    center_window(root)

    # End gui



    # Motor code
    # To launch with no_motor and no_emg, run sign_in.py and hold shift while you press continue
    frame = framework(options.port, patID=options.pat_id, sess=options.sess,
                      premin=preload_min, premax=preload_max, no_motor=no_motor, no_emg=no_emg)

    center_window(root)
    while root.running:
        # Update preload display
        if frame.mot:
            if frame.mot.torque_update:
                torque_value = frame.mot.torque_value
                frame.mot.torque_update = False
                preload_display.update_data(torque_value)

        # Pause button flashing
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

        if options.sess_updated:
            patient_info_lbl.configure(text=str(options.port) + " " + str(options.pat_id) + " " + str(options.sess))
            options.sess_updated = False

        # Check if a trial is just starting
        if frame.starting_trial:
            show_preload_display()
            general_info_lbl.configure(text="Begin Preloading...")
            general_info_lbl.last_updated = time.time()
            frame.starting_trial = False

        # Clear general info label after 3 seconds
        if time.time() - general_info_lbl.last_updated > GI_CLEAR_TIME:
            general_info_lbl.configure(text="")

        # This happens when after a trial
        if frame.show_emg:
            # TODO Update success_display to reflect success or failure
            position = random.random() * (m1display.max - m1display.min) * 0.7 + m1display.min + (m1display.max - m1display.min) * 0.3
            show_m1display(position)
            success_display.set_record(i, position < m1threshold)
            i += 1
            if i == nw * nh:
                i = 0
                success_display.reset_all()

            frame.show_emg = False
            if not no_emg:
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
           
        root.update()


if __name__ == "__main__":
    show_app(None, 1234, 1, no_motor=True, no_emg=True)
