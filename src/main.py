'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''


from tkinterdnd2 import DND_FILES, TkinterDnD #pip install tkinterdnd2
from HAPpy import HAPpy
from console_log import Logger

# -vf "scale=1280:720" -fast -infbuf -framedrop

# ---------------------------------------------------------------------------- #
#                                   CONSTANTS                                  #
# ---------------------------------------------------------------------------- #
APPNAME =  "HAPpy"
VERSION = "0.2.1"

# -------------------------------- PATCH NOTES ------------------------------- #
# fixed issue where massive files (specifically, videos from 360 cameras) would not be encoded

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
    app.setup_ui()

    result = console.create_log()

    if not result:
        pass
        console.log(app.encoder.get_version("ffmpeg"), "INIT")
        console.log(app.encoder.get_version("ffprobe"), "INIT")

    console.log(f"{APPNAME} v{VERSION} started", "INIT")

    root.mainloop()