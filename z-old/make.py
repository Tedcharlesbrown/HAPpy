from distutils.core import setup
import py2exe
import os
from cx_Freeze import setup, Executable
# from py2exe.freeze import Freeze

# Specify your main script
main_script = r"main.py"

# Specify additional scripts and modules to include
scripts_and_modules = [
    r"encode.py",
    r"src\__init__.py",
    r"src\encode_page.py",
    r"src\filehandler_page.py",
    r"src\gui_page.py"
]

# Specify additional data files (non-Python files)
data_files = [
    (r"GUI\assets", [
        r"GUI\assets\Background.png",
        r"GUI\assets\Button_ClearSelection.png",
        r"GUI\assets\Button_EncodeAll.png",
        r"GUI\assets\Button_EncodeSelected.png",
        r"GUI\assets\Button_RemoveFiles.png",
        r"GUI\assets\Button_SelectADestination.png",
        r"GUI\assets\Button_SelectAFile.png",
        r"GUI\assets\Button_SelectAFolder.png",
        r"GUI\assets\Checkbox_off.png",
        r"GUI\assets\Checkbox_on.png",
        r"GUI\assets\Popup_Background.png",
        r"GUI\assets\Popup_Skip.png",
        r"GUI\assets\Popup_Yes.png",
        r"GUI\assets\Popup_YesAll.png",
        r"GUI\assets\ProgressBar.png",
        r"GUI\assets\radio_off.png",
        r"GUI\assets\radio_on.png",
        r"GUI\assets\Tree_Destination.png",
        r"GUI\assets\Tree_DropArea.png",
        r"GUI\assets\LiberationSans-Bold.ttf",
        r"GUI\assets\LiberationSans-Regular.ttf",


    ]),
    ("FFMPEG", [
        r"FFMPEG\ffmpeg.exe",
        r"FFMPEG\ffprobe.exe"
    ])
]

flattened_data_files = []
for target, sources in data_files:
    for source in sources:
        flattened_data_files.append((source, target))

# Build options
build_options = {
    "optimize": 2,
    "excludes": [""],
    "includes": ["encodings"],
    "packages": ["encodings","tkinterdnd2"],
    "include_files": flattened_data_files,
}

setup(
    name="YourAppName",
    version="1.0",
    description="Your App Description",
    options={"build_exe": build_options},
    executables=[Executable(main_script)]
)