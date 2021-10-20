from tkinter import *
import random
from global_funcs import *

def show_app(port, pat_id, sess):
    root = Tk()
    root.configure(bg="white")

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
        success_lbl.configure(text="Successes: " + str(success_count))
        failure_lbl.configure(text="Failures: " + str(failure_count))

    def on_start():
        global success_record
        if random.random() < 0.5:
            success_record.append(True)
        else:
            success_record.append(False)
        update_successes()
    
    def trash_prev():
        global success_record
        success_record = success_record[0:-1]
        update_successes()

    big_w = 10
    big_h = 3
    start_btn = Button(root, text="Start", command=on_start, width=big_w, height=big_h,
            bg="green", font=button_font, fg=button_font_color)
    start_btn.grid(row=4, column=0, padx=padx, pady=pady)

    pause_btn = Button(root, text="Pause", width=big_w, height=big_h,
            bg="red", font=button_font, fg=button_font_color)
    pause_btn.grid(row=4, column=1, padx=padx, pady=pady)

    trash_btn = Button(root, text="Trash Prev\nResult", command=trash_prev, width=big_w, height=big_h,
            bg="blue", font=button_font, fg=button_font_color)
    trash_btn.grid(row=4, column=3, padx=padx, pady=pady)

    global success_lbl
    global failure_lbl
    success_lbl = Label(root)
    success_lbl.configure(bg="white")
    success_lbl.grid(row=3, column=0)
    failure_lbl = Label(root)
    failure_lbl.configure(bg="white")
    failure_lbl.grid(row=3, column=1)
    update_successes()

    root.geometry("800x500")
    root.mainloop()


if __name__ == "__main__":
    show_app("COM1", 1234, 1)
