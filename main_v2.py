from tkinterdnd2 import DND_FILES, TkinterDnD
from src import HAPPY

# import os
# import subprocess
# import queue
# from tkinter import ttk, filedialog, PhotoImage, font
# from tkinterdnd2 import DND_FILES, TkinterDnD
# from src import HAPPY
# import threading
# import tkinter as tk
# import ffmpeg  # ffmpeg-python

# import re
# import tkinter as tk
# from tkinter import ttk, filedialog, PhotoImage, font
# from functools import partial
# from tkinterdnd2 import DND_FILES, TkinterDnD
# from encode import Encoder


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("HAP.py")
    root.geometry("800x600")
    root.configure(bg="#2E2E2E")  # Dark background color
    
    app = HAPPY(root)
    
    root.mainloop()