
from os import stat
from time import sleep
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import filedialog, messagebox
from global_funcs import *

import statistics

from PIL import ImageTk, Image
from analysis_tools import *

from object_browser import Browser

folder_name = filedialog.askdirectory(title="Select Patient Folder")
if folder_name != "":
    
    sessions, multiple_patids = open_json_files(folder_name)
    
    if multiple_patids:
        messagebox.showwarning(
            "Data Loading Error!", "Loaded Blocks Contain Differeing Patient IDs")

    for sess in sessions.values():
        for blk in sess.values():
            blk_trls_avg_pre = []
            for trl in blk.trials:
                trl.pre_avg = statistics.mean(trl.emg_data[0:400])
                trl.pre_std = statistics.stdev(trl.emg_data[0:400])
                blk_trls_avg_pre.append(trl.pre_avg)
            
            blk.pre_avg_std = statistics.stdev(blk_trls_avg_pre)
            blk.pre_avg_avg = statistics.mean(blk_trls_avg_pre)

            print(f"Sess {blk.session} Block {blk.blocknum}'s standard deviation of preload is {blk.pre_avg_std}")
            print(f"Sess {blk.session} Block {blk.blocknum}'s mean of preload is {blk.pre_avg_avg}")
                
            


    with open(join(folder_name, f"cv_calcs.csv"), "w") as csv_file:
        
        # Block header
        csv_file.write(",")
        for sess in sessions.values():
            for blk in sess.values():
                csv_file.write(f"Sess{blk.session} Block {blk.blocknum},,")

        # Block value headers
        csv_file.write("\n,")
        for sess in sessions.values():
            for blk in sess.values():
                csv_file.write(f"Block preload avg, Block preload std,")

        # Block values
        csv_file.write("\n,")
        for sess in sessions.values():
            for blk in sess.values():
                csv_file.write(f"{blk.pre_avg_avg},{blk.pre_avg_std},")

        csv_file.write("\n")
        csv_file.write("Trials\n")

        trials =[[x] for x in range(0, 80)]

        for sess in sessions.values():
            for blk in sess.values():
                print(len(blk.trials))
                for i,trl in enumerate(blk.trials):
                    if trials[i]:
                        trials[i].append(trl.pre_avg)
                        trials[i].append(trl.pre_std)
                
        
        for row in trials:
            for item in row:
                csv_file.write(f"{item},")
            csv_file.write("\n")
