import sys
import os

def resource_path(relative_path, is_asset=True):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if is_asset:
        relative_path = os.path.join("GUI/assets", relative_path)
    else:
        relative_path = os.path.join("FFMPEG", relative_path)
    
    try:
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    except Exception:
        base_path = os.path.abspath(".")
        relative_path = os.path.relpath(relative_path)
        return os.path.join(os.path.dirname(base_path), relative_path)
