
from tkinter import *
from tkinter import filedialog, messagebox
from global_funcs import *

from PIL import ImageTk, Image
from analysis_tools import *



def show_analysis_app():

    root = Tk()
    root.title("LETREP2 Analysis")
    root.configure(bg="white")
    root.running = True

    def on_closing():
        root.running = False
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)

    def on_open():
        folder_name = filedialog.askdirectory(title="Select Patient Folder")
        if folder_name != "":
            sessions, multiple_patids = open_json_files(folder_name)
        
            if multiple_patids:
                messagebox.showwarning(
                    "Data Loading Error!", "Loaded Blocks Contain Differeing Patient IDs")

        

    # Button configuration
    big_w = 18
    big_h = 3

    # browse_button
    open_btn = Button(root, text="Open Patient Folder", command=on_open, width=big_w, height=big_h,
                       bg="blue", font=button_font, fg=button_font_color)
    open_btn.grid(row=1, column=0, padx=padx, pady=pady)

    img = Image.open(logo_dir)
    img = img.resize((100, 100), Image.ANTIALIAS)
    logo = ImageTk.PhotoImage(img)
    logo_label = Label(root, image=logo, bg="white")
    logo_label.grid(row=0, column=0, padx=padx, pady=pady)
    root.geometry("1200x600")
    center_window(root)


    while root.running:
        root.update()


if __name__ == "__main__":

    show_analysis_app()
