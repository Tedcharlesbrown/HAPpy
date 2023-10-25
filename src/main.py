from tkinterdnd2 import DND_FILES, TkinterDnD
from HAPpy import ENCODER
from console_log import Logger

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
    app = ENCODER(root, console)

    result = console.create_log()

    if not result:
        console.log(app.encoder.get_version("ffmpeg"), "INIT")
        console.log(app.encoder.get_version("ffprobe"), "INIT")

    console.log(f"{APPNAME} v{VERSION} started", "INIT")

    root.mainloop()