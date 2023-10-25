import tkinter as tk
import subprocess
import pyautogui
import pygetwindow as gw

FFPLAY_PATH = r"C:\Users\TedCh\OneDrive\Documents\GitHub\HAPpy\FFMPEG\ffplay.exe"
TEST_VIDEO_PATH = r"C:\Users\TedCh\OneDrive\Desktop\HAPPY TEST\First\samples\100kPeople_NotchLC.mov"

process = None

def play_video():
    global process
    cmd = [
        FFPLAY_PATH,
        '-vf', "scale=1280:720",
        '-fast',
        '-infbuf',
        '-framedrop',
        TEST_VIDEO_PATH
    ]
    process = subprocess.Popen(cmd)

import pygetwindow as gw

def pause_video():
    try:
        windows = gw.getWindowsWithTitle('')
        for win in windows:
            print(win.title)  # Print the title of each window
            if "ffplay" in win.title:
                win.activate()
                break
        pyautogui.press('p')  # Simulate pressing the 'p' key
    except Exception as e:
        print(f"Error pausing video: {e}")

#p

def seek_forward():
    if process and process.poll() is None:
        process.stdin.write(b's')  # 's' is the seek forward command for ffplay
        process.stdin.flush()

def seek_backward():
    if process and process.poll() is None:
        process.stdin.write(b'a')  # 'a' is the seek backward command for ffplay
        process.stdin.flush()

root = tk.Tk()
root.geometry('300x200')

# Buttons
btn_play = tk.Button(root, text="Play", command=play_video)
btn_play.pack(pady=10)

btn_pause = tk.Button(root, text="Pause", command=pause_video)
btn_pause.pack(pady=10)

btn_forward = tk.Button(root, text="Seek Forward", command=seek_forward)
btn_forward.pack(pady=10)

btn_backward = tk.Button(root, text="Seek Backward", command=seek_backward)
btn_backward.pack(pady=10)

root.mainloop()