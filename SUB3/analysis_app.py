
from tkinter import *
from tkinter import filedialog
from global_funcs import *
from more_options import *
from PIL import ImageTk, Image
from analysis_tools import *



def show_app():

    root = Tk()
    root.configure(bg="white")
    root.running = True

    def on_closing():
        root.running = False
        root.destroy()
        
    root.protocol("WM_DELETE_WINDOW", on_closing)

    folder_name = None

    def on_open():
        folder_name = filedialog.askdirectory(title="Select Patient Folder")
        open_json_files(folder_name)

        

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


    center_window(root)
    while root.running:
        root.update()


if __name__ == "__main__":

    show_app()
