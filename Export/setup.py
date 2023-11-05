# python3 /Users/tcb_mini/Documents/GitHub/HAPpy/Export/setup.py py2app
# hdiutil create -volname "HAPpy" -srcfolder /Users/tcb_mini/Documents/GitHub/HAPpy/Export/dist/HAPpy.app -ov -format UDZO HAPpy.dmg


from setuptools import setup
import glob

APP = ['/Users/tcb_mini/Documents/GitHub/HAPpy/src/main.py']
ASSETS_DIR = '/Users/tcb_mini/Documents/GitHub/HAPpy/GUI/Assets'
DATA_FILES = [
    ('FFMPEG', ['/Users/tcb_mini/Documents/GitHub/HAPpy/FFMPEG/ffmpeg', '/Users/tcb_mini/Documents/GitHub/HAPpy/FFMPEG/ffprobe']),
    ('GUI/assets', glob.glob(ASSETS_DIR + '/*')),
    ('tkinterdnd2/', ['/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/tkinterdnd2'])
]
OPTIONS = {
    'argv_emulation': False,
    'iconfile': '/Users/tcb_mini/Documents/GitHub/HAPpy/GUI/assets/icon.icns',
    'packages': ['tkinterdnd2'],
}

setup(
    app=APP,
    name='HAPpy',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
