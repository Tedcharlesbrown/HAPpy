'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

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