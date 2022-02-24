
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import filedialog, messagebox
from global_funcs import *

from PIL import ImageTk, Image
from analysis_tools import *


class analysis_app(Tk):
    def __init__(self):
        super().__init__()
        self.title("LETREP2 Analysis")
        self.configure(bg="white")
        self.running = True

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.cbs = []
        self.sessions = {}

        self.browsing = False
        self.browsing_dict = {}

        # Button configuration
        self.big_w = 32
        self.big_h = 3

        self.small_w = 10
        self.small_h = 1

        # browse_button
        self.open_btn = Button(self, text="Open Pat folder", command=self.on_open, width=self.big_w, height=self.big_h,
                        bg="blue", font=button_font, fg=button_font_color)
        self.open_btn.grid(row=1, column=0, padx=padx, pady=pady)

        # to csv Button
        self.csv_btn = Button(self, text="Convert to CSV", command=self.on_open, width=self.big_w, height=self.big_h,
                        bg="blue", font=button_font, fg=button_font_color)
        self.csv_btn.grid(row=2, column=0, padx=padx, pady=pady)

        # Browser frame
        self.browser_frame = Frame(self, )
        self.browser_frame.grid(row=1, column=1, columnspan = 4, rowspan = 4, padx=padx, pady=pady)

        img = Image.open(logo_dir)
        img = img.resize((100, 100), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(img)
        self.logo_label = Label(self, image=logo, bg="white")
        self.logo_label.photo = logo
        self.logo_label.grid(row=0, column=0, padx=padx, pady=pady)
        
        # Window Configuration
        # self.geometry("1200x600")
        center_window(self)
        self.title("BETA BETA BETA")


    def on_closing(self):
        self.running = False
        self.destroy()

    def on_browse_open(self):
        selected = self.browse_listbox.curselection()
        if selected:
            selected = selected[0]
            if "Session" in self.browse_listbox.get(selected):
                key = int(self.browse_listbox.get(selected).split()[1])
                self.on_browse_close(False)
                self.start_browse(self.browsing_dict[key], "Block")

            elif "Block" in self.browse_listbox.get(selected):

                key = int(self.browse_listbox.get(selected).split()[1])
                self.on_browse_close(False)
                # Convert trial list to dictionary
                to_browse = {i:trl for i,trl in enumerate(self.browsing_dict[key].trials)} 

                self.start_browse(to_browse, "Trial")

    
    def on_browse_goback(self):
        pass

    def on_browse_close(self, delete_sessions = True):
        self.browse_close_btn.destroy()
        self.browse_open_btn.destroy()
        self.browse_goback_btn.destroy()
        self.browse_listbox.destroy()

        if delete_sessions:
            self.sessions = {}

    def on_open(self):
        folder_name = filedialog.askdirectory(title="Select Patient Folder")
        if folder_name != "":
            
            self.sessions, multiple_patids = open_json_files(folder_name)
            
            if multiple_patids:
                messagebox.showwarning(
                    "Data Loading Error!", "Loaded Blocks Contain Differeing Patient IDs")
            
            self.start_browse(self.sessions, "Sessions")
            

    def convert_to_JSON(self):
        folder_name = filedialog.askdirectory(title="Select Where to Save CSV")
        for sess in self.sessions.values():
                sess_to_csv(sess, folder_name)
                messagebox.showinfo(
                    "Sessions to CSV!", f"Converted {len(self.sessions)} session(s) to csv")


    def start_browse(self, items_to_browse, items_type, multi_select = False):

        self.browsing_dict = items_to_browse

        # Create buttons for browsing
        self.browse_open_btn = Button(self.browser_frame,text="Open", command=self.on_browse_open, width=self.small_w, height=self.small_h,
                                      bg="blue", font=button_font, fg=button_font_color)
        self.browse_open_btn.grid(
            row=2, column=1, padx=padx, pady=pady, sticky=NE)

        self.browse_goback_btn = Button(self.browser_frame,text=chr(10229), command=self.on_browse_goback, width=self.small_w, height=self.small_h,
                                        bg="blue", font=button_font, fg=button_font_color)
        self.browse_goback_btn.grid(
            row=2, column=1, padx=padx, pady=pady, sticky=NW)

        self.browse_close_btn = Button(self.browser_frame,text="Close browser", command=self.on_browse_close, width=self.small_w * 2, height=self.small_h,
                                        bg="blue", font=button_font, fg=button_font_color)
        self.browse_close_btn.grid(
            row=3, column=1, padx=padx, pady=pady)

        # Create Listbox for data
        self.browse_listbox = Listbox(
            self.browser_frame, width=40, height=12, selectmode=multi_select)
        self.browse_listbox.grid(
            row=0, column=1, rowspan=2, padx=padx, pady=pady, sticky=S)

        for key, _ in items_to_browse.items():
            self.browse_listbox.insert(key, f'{items_type} {key}')

        

    
    def run(self):

        while self.running:
            if self.browsing:
                if self.browse_listbox.curselection():
                    self.browse_open_btn["state"] = NORMAL
                else:
                    self.browse_open_btn["state"] = DISABLED

            self.update()



if __name__ == "__main__":

    app = analysis_app()
    app.run()
