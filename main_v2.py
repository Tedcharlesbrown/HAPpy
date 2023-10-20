from tkinterdnd2 import DND_FILES, TkinterDnD
from src import HAPPY
import time

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