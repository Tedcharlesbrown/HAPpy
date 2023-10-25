from tkinterdnd2 import DND_FILES, TkinterDnD
from src import HAPPY
from console.console_log import Logger

# ---------------------------------------------------------------------------- #
#                                   CONSTANTS                                  #
# ---------------------------------------------------------------------------- #
APPNAME =  "HAPpy"
VERSION = "0.0.1"


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title(APPNAME)
    root.geometry("800x600")
    root.resizable(False, False)

    console = Logger(f".{APPNAME} Log.csv")
    console.set_header("TIME,TYPE,MESSAGE")
    app = HAPPY(root, console)

    result = console.create_log()

    if not result:
        console.log(app.encoder.get_version("ffmpeg"), "INIT")
        console.log(app.encoder.get_version("ffprobe"), "INIT")

    console.log(f"{APPNAME} v{VERSION} started", "INIT")

    # file_path = r"C:\Users\TedCh\OneDrive\Desktop\HAPPY TEST\First\version test\100kPeople_422_v1.mov"
    # app.trigger_overwrite_popup("The file already exists. Do you want to overwrite it?")
    # app.trigger_overwrite_popup(file_path)
    # app.trigger_overwrite_popup("ALERT!\nTHE FILE ALREADY EXISTS.\nDO YOU WANT TO OVERWRITE IT?")

    root.mainloop()