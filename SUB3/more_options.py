from tkinter import *
from global_funcs import *

class Options:
    def __init__(self, port, pat_id, sess):
        self.port = port
        self.pat_id = pat_id
        self.sess = sess
        self.sess_updated = False
    
    def copy(self):
        return Options(self.port, self.pat_id, self.sess)

    def impose_on(self, other):
        other.port = self.port
        other.pat_id = self.pat_id
        if other.sess != self.sess:
            other.sess = self.sess
            other.sess_updated = True
            print("sess_updated")
        else:
            other.sess = self.sess

def show_more_options(options):
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

    sess_label = Label(root, text="Session #:", bg="white", font=small_font)
    sess_label.grid(row=3, column=0, sticky="e")

    sess_choice = IntVar(root)
    sess_choice.set(options.sess)

    sess_list = range(1, 16)

    def sess_command(event):
        modified_options.sess = sess_choice.get()
    sess_selector = OptionMenu(
        root, sess_choice, *sess_list, command=sess_command)
    sess_selector.configure(width=5, anchor="w")
    sess_selector.grid(row=3, column=1, sticky="w")

    def exit():
        root.running = False
        root.destroy()

    def ok():
        modified_options.impose_on(options)
        exit()
        
    root.protocol("WM_DELETE_WINDOW", exit)

    ok_button = Button(root, text="Ok", command=ok, width=10, height=2)
    ok_button.grid(row=6, column=0, sticky="e", padx=padx, pady=pady)

    cancel_button = Button(root, text="Cancel", command=exit, width=10, height=2)
    cancel_button.grid(row=6, column=1, sticky="w", padx=padx, pady=pady)

    center_window(root)
    # root.mainloop()
    while root.running:
        root.update()

    


if __name__ == "__main__":
    show_more_options(Options('COM1', 1234, 4))
