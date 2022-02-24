from msilib.schema import CheckBox
from tkinter import *
from global_funcs import *
import logging

class Options:
    def __init__(self, port, pat_id, sess, pre_min = .4, pre_max = .5, display_T=False):
        self.port = port
        self.pat_id = pat_id
        self.sess = sess
        self.torque_display = display_T
        self.pre_min = pre_min
        self.pre_max = pre_max
        self.updates = False
        self.show_emg = False
        self.display_success = False
        
    
    def copy(self):
        return Options(self.port, self.pat_id, self.sess, self.torque_display)

    def impose_on(self, other):
        logging.debug("Imposing more options on options.")

        other.updates = True
        other.port = self.port
        other.pat_id = self.pat_id
        other.torque_display = self.torque_display
        other.pre_max = self.pre_max
        other.pre_min = self.pre_min
        other.show_emg = self.show_emg
        other.display_success = self.display_success
        if other.sess != self.sess:
            other.sess = self.sess
            logging.debug("sess_updated")
        else:
            other.sess = self.sess

def show_more_options(options):
    logging.debug("Displaying more options")
    root = Tk()
    root.running = True
    root.configure(bg="white")

    modified_options = options.copy()

    title_label = Label(root, text="More Options", bg="white", padx=padx, pady=pady, font=large_font)
    title_label.grid(row=0, column=0, columnspan=2)

    port_label = Label(root, text="Port:", bg="white", font=small_font)
    port_label.grid(row=1, column=0, sticky="e")

    port_text = Text(root, width=8, height=1, fg='gray')
    port_text.insert(1.0, str(options.port))
    port_text.configure(state='disabled')
    port_text.grid(row=1, column=1, sticky="w")

    id_label = Label(root, text="Patient ID:", bg="white", font=small_font)
    id_label.grid(row=2, column=0, sticky="e")
    
    id_text = Text(root, width=8, height=1, fg='gray')
    id_text.insert(1.0, str(options.pat_id))
    id_text.configure(state='disabled')
    id_text.grid(row=2, column=1, sticky="w")

    max_label = Label(root, text="Preload Max:", bg="white", font=small_font)
    max_label.grid(row=3,column=0,sticky="e")

    max_entry = Entry(root, width=8, fg='black')
    max_entry.insert(0, str(options.pre_max))
    max_entry.grid(row=3, column=1, sticky="w")

    min_label = Label(root, text="Preload Min:", bg="white", font=small_font)
    min_label.grid(row=4, column=0, sticky="e")

    min_entry = Entry(root, width=8, fg='black')
    min_entry.insert(0, str(options.pre_min))
    min_entry.grid(row=4, column=1, sticky="w")

    sess_label = Label(root, text="Session #:", bg="white", font=small_font)
    sess_label.grid(row=5, column=0, sticky="e")

    sess_choice = IntVar(root)
    sess_choice.set(options.sess)

    sess_list = range(1, 16)

    def sess_command(event):
        modified_options.sess = sess_choice.get()
    sess_selector = OptionMenu(
        root, sess_choice, *sess_list, command=sess_command)
    sess_selector.configure(width=5, anchor="w")
    sess_selector.grid(row=5, column=1, sticky="w")

    tor_disp = BooleanVar(root)
    tor_disp.set(options.torque_display)

    def tor_disp_command():
        modified_options.torque_display = tor_disp.get()
    torque_disp_checkbox = Checkbutton(root, bg='white', text='Display Torque',
                                       variable=tor_disp, onvalue=True, offvalue=False, command=tor_disp_command)
    torque_disp_checkbox.grid(row=6,column=0,columnspan=2)

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


    def exit():
        root.running = False
        root.destroy()

    def ok():
        modified_options.pre_min = float(min_entry.get())
        modified_options.pre_max = float(max_entry.get())
        modified_options.impose_on(options)
        exit()
        
    root.protocol("WM_DELETE_WINDOW", exit)

    ok_button = Button(root, text="Ok", command=ok, width=10, height=2)
    ok_button.grid(row=9, column=0, sticky="e", padx=padx, pady=pady)

    cancel_button = Button(root, text="Cancel", command=exit, width=10, height=2)
    cancel_button.grid(row=9, column=1, sticky="w", padx=padx, pady=pady)

    center_window(root)
    # root.mainloop()
    while root.running:
        root.update()

    


if __name__ == "__main__":
    show_more_options(Options('COM1', 1234, 4))
