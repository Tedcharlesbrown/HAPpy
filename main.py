from tkinterdnd2 import DND_FILES, TkinterDnD
from src import HAPPY
from console.console_log import Logger

# ---------------------------------------------------------------------------- #
#                                   CONSTANTS                                  #
# ---------------------------------------------------------------------------- #
APPNAME =  "HAP-PY"
VERSION = "0.0.1"


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title(APPNAME)
    root.geometry("800x600")

    console = Logger(f".{APPNAME} Log.csv")
    console.set_header("TIME,TYPE,MESSAGE")
    app = HAPPY(root, console)

    result = console.create_log()

    if not result:
        console.log(app.encoder.get_version("ffmpeg"), "INIT")
        console.log(app.encoder.get_version("ffprobe"), "INIT")

    console.log(f"{APPNAME} v{VERSION} started", "INIT")

    root.mainloop()