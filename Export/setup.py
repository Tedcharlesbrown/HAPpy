# python3 /Users/tcb_mini/Documents/GitHub/HAPpy/Export/setup.py py2app

from setuptools import setup

APP = ['/Users/tcb_mini/Documents/GitHub/HAPpy/src/main.py']
DATA_FILES = [
    ('FFMPEG', ['/Users/tcb_mini/Documents/GitHub/HAPpy/FFMPEG/ffmpeg', '/Users/tcb_mini/Documents/GitHub/HAPpy/FFMPEG/ffprobe']),
    ('GUI/assets', ['/Users/tcb_mini/Documents/GitHub/HAPpy/GUI/Assets']),
    ('tkinterdnd2/', ['/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/tkinterdnd2'])
]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': '/Users/tcb_mini/Documents/GitHub/HAPpy/GUI/assets/icon.icns',
    'packages': ['tkinterdnd2'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
