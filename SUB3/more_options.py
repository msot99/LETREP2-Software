from tkinter import *
from global_funcs import *
import logging
from OptionWidgets import *

option_columns = [
        [
            IntOption("pat_id", "Patient ID:", 1234),
            FloatOption("pre_max", "Preload Max:", 0.3),
            FloatOption("pre_min", "Preload Min:", 0.4),
            BooleanOption("torque_display", "Display Torque", False),
            BooleanOption("show_emg", "Show EMG", True),
            BooleanOption("display_success", "Display Success", True)
        ],
        [
            FloatOption("m1_max", "M1 Max:", 5),
            FloatOption("m1_min", "M1 Min:", 0),
            FloatOption("m1_thresh", "M1 Threshold:", 1.3),
            DropdownOption("sess", "Session #:", range(1, 16), 1)
        ]
    ]

def get_default_options():
    return dict([(option.name, option.value) for collist in option_columns for option in collist] + [("updates", False)])

def show_more_options(options):
    logging.debug("Displaying more options")
    root = Tk()
    root.running = True
    root.configure(bg="white")

    gridy = 0

    title_label = Label(root, text="More Options", bg="white", padx=padx, pady=pady, font=large_font)
    title_label.grid(row=gridy, column=0, columnspan=2*len(option_columns))
    gridy += 1

    for column, collist in enumerate(option_columns):
        for row, option in enumerate(collist):
            option.value = options[option.name]
            option.grid(root, row+1, 2*column)
            gridy = max(gridy, row+1)
    
    gridy += 1


    def on_exit():
        root.running = False
        root.destroy()

    def on_ok():
        for collist in option_columns:
            for option in collist:
                options[option.name] = option.get_value()
        options["updates"] = True
        print(options)
        on_exit()
        
    root.protocol("WM_DELETE_WINDOW", on_exit)

    ok_button = Button(root, text="Ok", command=on_ok, width=10, height=2)
    ok_button.grid(row=gridy, column=2*len(option_columns)-2, sticky="e", padx=padx, pady=pady)

    cancel_button = Button(root, text="Cancel", command=on_exit, width=10, height=2)
    
    cancel_button.grid(row=gridy, column=2*len(option_columns)-1, sticky="w", padx=padx, pady=pady)
    gridy += 1

    center_window(root)
    # root.mainloop()
    while root.running:
        root.update()

    


if __name__ == "__main__":
    show_more_options(get_default_options())
