import tkinter as tk 
from tkinter import ttk, filedialog
from tkinter import *
import os
import threading
from utils import start_main_download_process, get_current_progress

root = tk.Tk()
root.title("Spotify Downloader")
root.configure(bg="#121212") 
root.minsize(600, 700)  

MAIN_BG_COLOR = "#121212"  
MAIN_FG_COLOR = "#FFFFFF"
BUTTON_BG_COLOR = "#1DB954" 
BUTTON_FG_COLOR = "#FFFFFF"
ENTRY_BG_COLOR = "#212121"  


padding_frame = tk.Frame(root, bg=MAIN_BG_COLOR, padx=20, pady=20)
padding_frame.pack(fill=BOTH, expand=True)

main_frame = tk.Frame(padding_frame, bg=MAIN_BG_COLOR)
main_frame.pack(fill=BOTH, expand=True)

def initDownload():
    URLS = playlist_entries.get("1.0", "end-1c").splitlines()
    if folder_path_label.cget("text") == "current directory":
        savePath = os.getcwd()
    else:
        savePath = folder_path_label.cget("text")

    root.after(100, check_progress)
    
    try:
        write_to_output("Starting download process...")
       
        start_main_download_process(URLS, savePath, write_to_output)
        
        write_to_output("Download complete!")
    except Exception as e:
        write_to_output(f"Error: {str(e)}")
    finally:
        
        root.after(0, lambda: download_button.config(state=NORMAL))

def write_to_output(text):
    output.config(state=NORMAL)
    output.insert(END, text + "\n")
    output.see(END) 
    output.config(state=DISABLED)

def check_progress():
    progress = get_current_progress()
    
  
    progress_bar['value'] = progress
    root.update_idletasks()
    
   
    if progress < 100:
        root.after(100, check_progress)

def update_progress_bar(progress):
    progress_bar['value'] = progress
    root.update_idletasks()

def startDownloadThread():

    progress_bar['value'] = 0
    root.update_idletasks()  
    
    
    download_button.config(state=DISABLED)
 
    download_thread = threading.Thread(target=initDownload, daemon=True)
    download_thread.start()

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path_label.config(text=folder_selected)
    else:
        folder_path_label.config(text="current directory")

title_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR)
title_frame.pack(fill=X, pady=(0, 10))

title1 = tk.Label(title_frame, text="Spotify Downloader", font=("Helvetica", 28, "bold"), bg=MAIN_BG_COLOR, fg="#1DB954")
title1.pack(pady=(0, 5))

title2 = tk.Label(main_frame, text="Enter Spotify Playlist or Album URLs line by line", font=("Helvetica", 12), bg=MAIN_BG_COLOR, fg=MAIN_FG_COLOR)
title2.pack(pady=(0, 10))


input_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR, bd=1, relief=SOLID)
input_frame.pack(fill=X, pady=10, padx=10)

playlist_entries = Text(input_frame, height=12, width=50, bg=ENTRY_BG_COLOR, fg=MAIN_FG_COLOR, insertbackground='white', font=("Helvetica", 11), bd=0)
playlist_entries.pack(fill=BOTH, expand=True, padx=2, pady=2)


options_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR)
options_frame.pack(fill=X, pady=10)

folder_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR)
folder_frame.pack(fill=X, pady=10)

folder_path_select_button = tk.Button(folder_frame, text="Select Download Folder", command=select_folder, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=("Helvetica", 11),padx=10, pady=5, bd=0)
folder_path_select_button.pack(side=LEFT, padx=(10, 5))

folder_path_label = tk.Label(folder_frame, text="current directory", bg=MAIN_BG_COLOR, fg="#AAAAAA", font=("Helvetica", 11))
folder_path_label.pack(side=LEFT, padx=5, fill=X)


button_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR)
button_frame.pack(fill=X, pady=10)

download_button = tk.Button(button_frame, text="Download", command= startDownloadThread, bg=BUTTON_BG_COLOR, fg=BUTTON_FG_COLOR, font=("Helvetica", 12, "bold"),padx=20, pady=8, bd=0)
download_button.pack(pady=10, fill=X, padx=80)


output_label = tk.Label(main_frame, text="Console Output", font=("Helvetica", 12), bg=MAIN_BG_COLOR, fg=MAIN_FG_COLOR)
output_label.pack(anchor=W, padx=10, pady=(20, 5))

output_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR, bd=1, relief=SOLID)
output_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

output = tk.Text(output_frame, height=8, width=50, bg=ENTRY_BG_COLOR, fg="#AAAAAA", font=("Courier", 10), bd=0, state=DISABLED)
output.pack(fill=BOTH, expand=True, padx=2, pady=2)


progress_frame = tk.Frame(main_frame, bg=MAIN_BG_COLOR)
progress_frame.pack(fill=X, pady=(0, 10), padx=10)

progress_bar = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=300, mode='determinate')
progress_bar.pack(fill=X)


style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=8, troughcolor=ENTRY_BG_COLOR, 
               background=BUTTON_BG_COLOR, borderwidth=0)

root.mainloop()
