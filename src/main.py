from tkinterdnd2 import DND_FILES, TkinterDnD
from HAPpy import HAPpy
from console_log import Logger

# -vf "scale=1280:720" -fast -infbuf -framedrop

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
    app = HAPpy(root, console)
    app.setup_ui(True)

    result = console.create_log()

    if not result:
        console.log(app.encoder.get_version("ffmpeg"), "INIT")
        console.log(app.encoder.get_version("ffprobe"), "INIT")

    console.log(f"{APPNAME} v{VERSION} started", "INIT")

    # print(app.trigger_overwrite_popup("test"))

    root.mainloop()


# from HAPpy.gui_class import GUI


# root = TkinterDnD.Tk()
# root.title(APPNAME)
# root.geometry("800x600")
# root.resizable(False, False)

# gui = GUI(root)
# gui.setup_constants()
# gui.configure_styles()
# gui.setup_ui()

# root.mainloop()
