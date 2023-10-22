from tkinterdnd2 import DND_FILES, TkinterDnD
from src import HAPPY
from console.console_log import Logger


APPNAME =  "HAP-PY"
VERSION = "0.0.1"

console = Logger(f"{APPNAME} Log.csv")

console.set_header("TIME,MESSAGE,ALERT")
console.create_log()
console.log(f"{APPNAME} v{VERSION} started")
# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title(APPNAME)
    root.geometry("800x600")
    root.configure(bg="#2E2E2E")  # Dark background color
    
    # app = HAPPY(root)

    root.mainloop()