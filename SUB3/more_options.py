from msilib.schema import CheckBox
from tkinter import *
from global_funcs import *
import logging


def show_more_options(options):
    logging.debug("Displaying more options")
    root = Tk()
    root.running = True
    root.configure(bg="white")

    modified_options = options.copy()

    title_label = Label(root, text="More Options", bg="white", padx=padx, pady=pady, font=large_font)
    title_label.grid(row=0, column=0, columnspan=2)

    id_label = Label(root, text="Patient ID:", bg="white", font=small_font)
    id_label.grid(row=1, column=0, sticky="e")
    
    id_entry = Entry(root, width=8)
    id_entry.insert(0, str(options["pat_id"]))
    id_entry.grid(row=1, column=1, sticky="w")

    pre_max_label = Label(root, text="Preload Max:", bg="white", font=small_font)
    pre_max_label.grid(row=2,column=0,sticky="e")

    pre_max_entry = Entry(root, width=8)
    pre_max_entry.insert(0, str(options["pre_max"]))
    pre_max_entry.grid(row=2, column=1, sticky="w")

    pre_min_label = Label(root, text="Preload Min:", bg="white", font=small_font)
    pre_min_label.grid(row=3, column=0, sticky="e")

    pre_min_entry = Entry(root, width=8)
    pre_min_entry.insert(0, str(options["pre_min"]))
    pre_min_entry.grid(row=3, column=1, sticky="w")

    m1_max_label = Label(root, text="M1 Max:", bg="white", font=small_font)
    m1_max_label.grid(row=4, column=0, sticky="e")

    m1_max_entry = Entry(root, width=8)
    m1_max_entry.insert(0, str(options["m1_max"]))
    m1_max_entry.grid(row=4, column=1, sticky="w")

    m1_min_label = Label(root, text="M1 Min:", bg="white", font=small_font)
    m1_min_label.grid(row=5, column=0, sticky="e")

    m1_min_entry = Entry(root, width=8)
    m1_min_entry.insert(0, str(options["m1_min"]))
    m1_min_entry.grid(row=5, column=1, sticky="w")

    m1_thresh_label = Label(root, text="M1 Threshold:", bg="white", font=small_font)
    m1_thresh_label.grid(row=6, column=0, sticky="e")

    m1_thresh_entry = Entry(root, width=8)
    m1_thresh_entry.insert(0, str(options["m1_thresh"]))
    m1_thresh_entry.grid(row=6, column=1, sticky="w")

    sess_label = Label(root, text="Session #:", bg="white", font=small_font)
    sess_label.grid(row=7, column=0, sticky="e")

    sess_choice = IntVar(root)
    sess_choice.set(options["sess"])

    sess_list = range(1, 16)

    def sess_command(event):
        modified_options["sess"] = sess_choice.get()
    sess_selector = OptionMenu(
        root, sess_choice, *sess_list, command=sess_command)
    sess_selector.configure(width=5, anchor="w")
    sess_selector.grid(row=7, column=1, sticky="w")

    tor_disp = BooleanVar(root)
    tor_disp.set(options["torque_display"])

    def tor_disp_command():
        modified_options["torque_display"] = tor_disp.get()
    torque_disp_checkbox = Checkbutton(root, bg='white', text='Display Torque',
                                       variable=tor_disp, onvalue=True, offvalue=False, command=tor_disp_command)
    torque_disp_checkbox.grid(row=8,column=0,columnspan=2)

    emg_plot = BooleanVar(root)
    emg_plot.set(options.show_emg)

    def show_emg_command():
        modified_options.show_emg = emg_plot.get()
    emg_plot_checkbox = Checkbutton(root, bg='white', text='Plot Emg/Acc',
                                    variable=emg_plot, onvalue=True, offvalue=False, command=show_emg_command)
    emg_plot_checkbox.grid(row=7, column=0, columnspan=2)

    suc_disp = BooleanVar(root)
    suc_disp.set(options.display_success)

    def suc_disp_command():
        modified_options.display_success = suc_disp.get()
    suc_disp_checkbox = Checkbutton(root, bg='white', text='Display Successes',
                                    variable=suc_disp, onvalue=True, offvalue=False, command=suc_disp_command)
    suc_disp_checkbox.grid(row=8, column=0, columnspan=2)


    def on_exit():
        root.running = False
        root.destroy()

    def on_ok():
        modified_options["pat_id"] = int(id_entry.get())
        modified_options["pre_min"] = float(pre_min_entry.get())
        modified_options["pre_max"] = float(pre_max_entry.get())
        modified_options["m1_max"] = float(m1_max_entry.get())
        modified_options["m1_min"] = float(m1_min_entry.get())
        modified_options["m1_thresh"] = float(m1_thresh_entry.get())
        options.update(modified_options)
        options["updates"] = True
        print(options)
        on_exit()
        
    root.protocol("WM_DELETE_WINDOW", on_exit)

    ok_button = Button(root, text="Ok", command=on_ok, width=10, height=2)
    ok_button.grid(row=9, column=0, sticky="e", padx=padx, pady=pady)

    cancel_button = Button(root, text="Cancel", command=on_exit, width=10, height=2)
    
    cancel_button.grid(row=9, column=1, sticky="w", padx=padx, pady=pady)

    center_window(root)
    # root.mainloop()
    while root.running:
        root.update()

    


if __name__ == "__main__":
    show_more_options({
        "pat_id": 1234,
        "sess": 1,
        "pre_max": 0.3,
        "pre_min": 0.4,
        "m1_max": 0,
        "m1_min": 5,
        "m1_thresh": 1.3,
        "torque_display": False
    })
