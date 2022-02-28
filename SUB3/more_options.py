from tkinter import *
from global_funcs import *
import logging
from OptionWidgets import *

option_columns = [
        [
            FloatOption("pre_max", "Preload Max:", 0.3),
            FloatOption("pre_min", "Preload Min:", 0.4),
            FloatOption("peak_min_threshold", "EMG Peak Threshold:", 0.06),
            FloatOption("avg_peak_delay", "EMG Peak Delay:", 42),
            BooleanOption("display_success", "Display Success", True),
            BooleanOption("preload_audio", "Preload Audio Notification", True),
            BooleanOption("torque_display", "Display Torque", False),
            BooleanOption("show_emg", "Show EMG", True)
        ],
        [
            FloatOption("m1_max", "M1 Max:", 0.1),
            FloatOption("m1_min", "M1 Min:", 0),
            FloatOption("m1_thresh", "M1 Threshold:", 1.3),
            IntOption("pat_id", "Patient ID:", 1234),
            DropdownOption("sess", "Session #:", range(1, 16), 1),
            DropdownOption("block_count", "Block:", range(1, 14), 1)
        ]
    ]

def get_default_options():
    return dict([(option.name, option.value) for collist in option_columns for option in collist] + [("updates", False)])

def show_more_options(options):
    logging.debug("Displaying more options")
    root = Tk()
    root.running = True
    root.configure(bg="white")

    title_label = Label(root, text="More Options", bg="white", padx=padx, pady=pady, font=large_font)
    title_label.grid(row=0, column=0, columnspan=2*len(option_columns))
    pre_column = 1

    for column, collist in enumerate(option_columns):
        for row, option in enumerate(collist):
            option.value = options[option.name]
            option.grid(root, row+pre_column, 2*column)


    def on_exit():
        root.running = False

    def on_ok():
        for collist in option_columns:
            for option in collist:
                options[option.name] = option.get_value()
        options["updates"] = True
        logging.info(options)
        on_exit()
        
    root.protocol("WM_DELETE_WINDOW", on_exit)

    max_height = max([len(collist) for collist in option_columns])
    ok_y = len(option_columns[-1])
    rowspan = max(max_height - ok_y, 1)
    ok_y += pre_column

    ok_button = Button(root, text="Ok", command=on_ok, width=10, height=2)
    ok_button.grid(row=ok_y, column=2*len(option_columns)-2, sticky="se", padx=padx, pady=pady, 
        rowspan=rowspan)

    cancel_button = Button(root, text="Cancel", command=on_exit, width=10, height=2)
    
    cancel_button.grid(row=ok_y, column=2*len(option_columns)-1, sticky="sw", padx=padx, pady=pady,
        rowspan=rowspan)

    center_window(root)
    # root.mainloop()
    while root.running:
        root.update()
    root.destroy()

    


if __name__ == "__main__":
    show_more_options(get_default_options())
