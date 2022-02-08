from tkinter import *
from global_funcs import *

def show_more_options(port, pat_id, sess, no_motor, no_emg):
    root = Tk()
    root.configure(bg="white")

    title_label = Label(root, text="More Options", bg="white", padx=padx, pady=pady, font=large_font)
    title_label.grid(row=0, column=0, columnspan=2)

    port_label = Label(root, text="Port:", bg="white", font=small_font)
    port_label.grid(row=1, column=0, sticky="e")

    port_text = Text(root, width=8, height=1, fg='gray')
    port_text.insert(1.0, port)
    port_text.configure(state='disabled')
    port_text.grid(row=1, column=1, sticky="w")

    id_label = Label(root, text="Patient ID:", bg="white", font=small_font)
    id_label.grid(row=2, column=0, sticky="e")
    
    id_text = Text(root, width=8, height=1, fg='gray')
    id_text.insert(1.0, str(pat_id))
    id_text.configure(state='disabled')
    id_text.grid(row=2, column=1, sticky="w")

    sess_label = Label(root, text="Session #:", bg="white", font=small_font)
    sess_label.grid(row=3, column=0, sticky="e")

    sess_choice = IntVar(root)
    sess_choice.set(1)

    sess_list = range(2, 16)

    sess_selector = OptionMenu(
        root, sess_choice, sess_choice.get(), *sess_list)
    sess_selector.configure(width=5, anchor="w")
    sess_selector.grid(row=3, column=1, sticky="w")

    def exit():
        pass

    def ok():
        
        exit()

    ok_button = Button(root, text="Ok", command=ok, width=10, height=2)
    ok_button.grid(row=6, column=0, sticky="e", padx=padx, pady=pady)

    cancel_button = Button(root, text="Cancel", command=exit, width=10, height=2)
    cancel_button.grid(row=6, column=1, sticky="w", padx=padx, pady=pady)

    center_window(root)
    root.mainloop()

    


if __name__ == "__main__":
    show_more_options('COM1', 1234, 1, True, True)
