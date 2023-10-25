import sys
import os

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     if relative_path.endswith(".png") or relative_path.endswith(".ico"):
#         relative_path = os.path.join("../GUI/assets", relative_path)
#     elif relative_path.endswith(".exe"):
#         relative_path = os.path.join("../FFMPEG", relative_path)
#     path = relative_path[3:]
#     try:
#         base_path = sys._MEIPASS
#         print(f"MEIPASS: {os.path.join(base_path, path)}")
#     except Exception:
#         base_path = os.path.abspath(".")
#         print(f"BASE_PATH: {base_path}")
#     return os.path.join(base_path, path)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if relative_path.endswith(".png") or relative_path.endswith(".ico"):
        relative_path = os.path.join("GUI/assets", relative_path)
    elif relative_path.endswith(".exe"):
        relative_path = os.path.join("FFMPEG", relative_path)
    
    try:
        base_path = sys._MEIPASS
        # print(f"MEIPASS: {os.path.join(base_path, relative_path)}")
        return os.path.join(base_path, relative_path)
    except Exception:
        base_path = os.path.abspath(".")
        relative_path = os.path.relpath(relative_path)
        # print(f"PATH: {os.path.join(os.path.dirname(base_path), relative_path)}")
        return os.path.join(os.path.dirname(base_path), relative_path)
    