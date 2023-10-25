import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if relative_path.endswith(".png") or relative_path.endswith(".ico"):
        relative_path = os.path.join("../GUI/assets", relative_path)
    elif relative_path.endswith(".exe"):
        relative_path = os.path.join("../FFMPEG", relative_path)
    # print(relative_path)
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)