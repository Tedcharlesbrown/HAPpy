import os
import sys

def resource_path(relative_path, is_asset=True):
    """ Get absolute path to resource, works for development, py2app, and PyInstaller """
    
    # Determine if it's an asset or a different type of file
    if is_asset:
        relative_path = os.path.join("GUI/assets", relative_path)
    else:
        relative_path = os.path.join("FFMPEG", relative_path)
    
    if getattr(sys, 'frozen', False):
        # The application is frozen
        if sys.platform == "darwin":
            # We are on macOS (py2app)
            base_path = os.path.dirname(sys.executable)
            return os.path.join(base_path, '..', 'Resources', relative_path)
        elif sys.platform == "win32":
            # We are on Windows (PyInstaller)
            base_path = sys._MEIPASS
            return os.path.join(base_path, relative_path)
    else:
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)