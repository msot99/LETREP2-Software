from datetime import datetime
import os
from tkinter import *
import time
import random

from PreloadDisplay import PreloadDisplay
from global_funcs import *
from more_options import *
from framework import framework
import peak
import matplotlib.pyplot as plt
from SuccessRecordDisplay import SuccessRecordDisplay
from PIL import ImageTk, Image
import logging

# Displays the most recent trial using matplotlib
def plot_emg(trial):
    emg_dc_offset = sum(trial.emg_data[0:400])/400

    yemg = [sample-emg_dc_offset for sample in trial.emg_data]

    yemg = trial.emg_data[400:800]
    yacc = trial.acc_data[400:800]

    _, ax = plt.subplots()
    
    ax.plot(yemg, 'r', label="EMG")
    ax.legend(loc=2)
    
    ax2 = ax.twinx()
    ax2.plot(yacc,'b', label="ACC")
    ax2.legend(loc=1)

    # Format plot
    plt.title('Most Recent Trial Readings')
    plt.ion()
    plt.legend()
    plt.show()
    plt.pause(5)
    plt.close()



def show_app(port, pat_id, sess, no_motor=False, no_emg=False):
    
    log_dir = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\LETREP2\\Logs\\')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=log_dir+datetime.now().strftime('Run_%Y-%m-%d_%H-%M.log'), level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s:%(message)s')


    root = Tk()
    root.configure(bg="white")
    root.running = True

    options = Options(port, pat_id, sess, pre_max=.3, pre_min=.4)

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

    patient_info_lbl = Label(root, text="PatID " + str(options.pat_id) + "\nSession #" + str(options.sess))
    patient_info_lbl.configure(bg="white", font=large_font)
    patient_info_lbl.grid(row=0, column=1)

    # Start, Pause, Trash, Stop, and Other button functions
    def on_start():
        frame.start_block()

    def on_pause():
        frame.pause_block()

    def trash_prev():
        pass
    
    def on_other_options():
        show_more_options(options)

    def on_stop():
        frame.stop_block()
        general_info_lbl.configure(text="Stopped")
        general_info_lbl.last_updated = time.time()
        

    # Button configuration
    big_w = 11
    big_h = 3

    # start_btn
    start_btn = Button(root, text="Start Block", command=on_start, width=big_w, height=big_h,
                       bg="green", font=button_font, fg=button_font_color)
    start_btn.grid(row=1, column=0, padx=padx, pady=pady)

    # pause_btn
    pause_btn_color_swap = True
    swap_time = 0
    PAUSE_BLINK_RATE = .5
    pause_btn = Button(root, text="Pause Block", command=on_pause, width=big_w, height=big_h,
                       bg="red", font=button_font, fg=button_font_color)
    pause_btn.grid(row=2, column=0, padx=padx, pady=pady)

    # trash_btn
    trash_btn = Button(root, text="Trash Prev\nResult", command=trash_prev, width=big_w, height=big_h,
                       bg="blue", font=button_font, fg=button_font_color)
    trash_btn.grid(row=0, column=2)

    # stop_btn
    stop_btn = Button(root, text="Stop Block", command=on_stop, width=big_w, height=big_h,
                        bg="gray", font=button_font, fg=button_font_color)
    stop_btn.grid(row=3, column=0, padx=padx, pady=pady)

    # other_opts_btn
    other_opts_btn = Button(root, text="More Options", command=on_other_options, width=big_w, height=big_h,
                        bg="gray", font=button_font, fg=button_font_color)
    other_opts_btn.grid(row=0, column=3)


    # Display Frame: widget to hold preload and record displays
    # display_frame
    df_bg = "gray"
    display_frame = Frame(root, bg=df_bg, padx=padx, pady=pady)

    df_block = Label(display_frame, text="Current Block: N/A", 
                     bg=df_bg, font=small_font)
    df_block.grid(row=0, column=0)

    df_trial = Label(display_frame, text="Current Trial: N/A",
                     bg=df_bg, font=small_font)
    df_trial.grid(row=0, column=1)

    df_torque = Label(display_frame, text="",
                     bg=df_bg, font=small_font)
    df_torque.grid(row=1, column=0)

    df_failure_lbl = Label(display_frame, text="Failure Reason!!", bg=df_bg, font=small_font, fg="red")
    df_failure_lbl.grid(row=1, column=0, columnspan=3)

    nw = 15
    nh = 5
    success_display = SuccessRecordDisplay(
        display_frame, 600, 220, nw, nh, margin=15, radius=15)
    success_display.grid(row=2, column=0, rowspan=2, columnspan=3)
    success_display.configure(bg=df_bg)

    preload_lbl = Label(display_frame, text="Preload Status", bg=df_bg, font=small_font)
    preload_lbl.grid(row=2, column=3)
    preload_display = PreloadDisplay(display_frame, 100, 200, options.pre_min, options.pre_max)
    preload_display.grid(row=3, column=3)
    preload_display.configure(bg=df_bg)

    GI_CLEAR_TIME = 3
    general_info_lbl = Label(display_frame, text="", bg=df_bg, font=large_font)
    general_info_lbl.grid(row=4, column=0, columnspan=4)
    general_info_lbl.last_updated = time.time()

    display_frame.grid(row=1, column=1, rowspan=3, columnspan=3)


    # root.geometry("1200x600")
    center_window(root)
    torque_value = 0

    # End gui

    # To launch with no_motor and no_emg, run sign_in.py and hold shift while you press continue
    frame = framework(options.port, patID=options.pat_id, sess=options.sess,
                      premin=options.pre_min, premax=options.pre_max, no_motor=no_motor, no_emg=no_emg)
    max = []
    center_window(root)
    while root.running:
        # Update preload display
        if frame.mot:
            if frame.mot.torque_update:
                torque_value = frame.mot.torque_value
                frame.mot.torque_update = False
                preload_display.update_data(torque_value)
                
                # Take a 20 sample rolling torque average
                if options.torque_display:
                    max.append(abs(torque_value))
                    max = max[-20:]
                    avg_torque = sum(max)/len(max)
                    df_torque.configure(text="Preload Value: %.4f" % avg_torque)
                else:
                    df_torque.configure(text="")
                           


        # Pause button flashing
        if frame.paused:

            other_opts_btn['state'] = 'normal'

            if pause_btn_color_swap and time.time() - swap_time > PAUSE_BLINK_RATE:
                pause_btn_color_swap = not pause_btn_color_swap
                pause_btn.configure(bg="red")
                swap_time = time.time()

            elif not pause_btn_color_swap and time.time() - swap_time > PAUSE_BLINK_RATE:
                pause_btn_color_swap = not pause_btn_color_swap
                pause_btn.configure(bg="green")
                swap_time = time.time()
        else:
            if not frame.running:
                other_opts_btn['state'] = 'normal'
            else:
                other_opts_btn['state'] = 'disabled'

            pause_btn.configure(bg="red")

        # Check for updates and then change values
        if options.updates:
            #Update preload values
            frame.update_preloads(options.pre_min,options.pre_max)
            preload_display.update_preloads(options.pre_min,options.pre_max)

            #Update session value
            patient_info_lbl.configure(text=str(options.port) + " " + str(options.pat_id) + " " + str(options.sess))
            options.updates = False


        # Check if a trial is just starting
        if frame.starting_trial:
            df_trial.configure(text="Current Trial: " + str(frame.trial_count+1))
            #Check if this is a first trial
            if frame.trial_count == 0:
                df_block.configure(text="Current Block: " + str(frame.block_count))
                success_display.reset_all()
            general_info_lbl.configure(text="Begin Preloading...")
            general_info_lbl.last_updated = time.time()
            frame.starting_trial = False

        # Clear general info label after 3 seconds
        if time.time() - general_info_lbl.last_updated > GI_CLEAR_TIME:
            general_info_lbl.configure(text="")

        # This happens when after a trial
        if frame.finished_trial:

            # Check if we are to show_emg
            if options.show_emg:
                plot_emg(frame.current_trial)

            # Remove DC Offset for finding peak
            emg_dc_offset = sum(frame.current_trial.emg_data[0:400])/400
            emg = [sample-emg_dc_offset for sample in frame.current_trial.emg_data]

            # Find Peak
            frame.current_trial.peak, frame.current_trial.max_delay_ms = peak.simple_peak(emg)

            # Update successs dispaly
            if options.display_success:
                # TODO Calculate success
                success_display.set_record(frame.trial_count, random.randint(0, 1))
            else:
                success_display.set_record(frame.trial_count, 3)
            
            # Reset trial bit
            frame.finished_trial = False

            # Check if we can do another trial
            if frame.trial_count+1 == nw * nh :
                logging.warning("Trial count meets success display limit... Ending block")
                frame.stop_block()
            

        root.update()


if __name__ == "__main__":

    show_app(None, 1234, 1, no_motor=True, no_emg=True)

