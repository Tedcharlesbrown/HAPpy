import tkinter as tk
from tkinter import filedialog


def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename(title="Select a file")
    return filepath

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folderpath = filedialog.askdirectory(title="Select a destination folder")
    return folderpath