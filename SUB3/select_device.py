from tkinter import *
from PIL import ImageTk, Image
import serial
import serial.tools.list_ports

from global_funcs import *
from sign_in import *


def select_device():
    root = Tk()
    root.configure(bg="white")

    ports = serial.tools.list_ports.comports()
    port_names = [x[0] + ": " + x[1] for x in ports]
    print(ports)

    img = Image.open(logo_dir)
    img = img.resize((250, 250), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(img)
    logo_label = Label(root, image=logo, bg="white")
    logo_label.grid(row=0, column=0, columnspan=2)

    label = Label(root, text="Select device:", bg="white", font=small_font)
    label.grid(row=1, column=0)

    choice = StringVar(root)
    unselected_port = "Select"
    choice.set(unselected_port)

    def continue_button():
        port = choice.get()
        if port == unselected_port:
            return
        root.destroy()
        sign_in(port.split(": ")[0])

    def update_button(port):
        if port == unselected_port:
            cont["state"] = "disabled"
        else:
            cont["state"] = "normal"

    selector = OptionMenu(root, choice, choice.get(), *
                          port_names, command=update_button)
    selector.configure(width=30, anchor="w")
    selector.grid(row=1, column=1)

    cont = Button(root, text="Continue", command=continue_button,
                  width=17, height=0, bg=button_color, font=button_font, fg=button_font_color)
    cont["state"] = "disabled"
    cont.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady)

    center_window(root)
    root.mainloop()


if __name__ == "__main__":
    select_device()
