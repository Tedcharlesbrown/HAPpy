'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

import sys
import json
from encode import FFMPEG
import tkinter as tk
from tkinter.ttk import *

import time
from pynput.keyboard import Key, Controller
import pygetwindow as gw

class Player:
    keyboard = Controller()
    ffplay = FFMPEG()

    INPUT_FILE = None
    FILE_INFO = None

    def parse(self, info):
        info = json.dumps(info, indent=3)
        print(info)
        return info

    def control_popup(self, info):
        root = tk.Tk()
        root.title("HAPpy Control")
        root.geometry("800x600")
        root.resizable(False, False)

        buttons = []

        buttons.append(tk.Button(root, text="Quit", command=lambda: player.control('q')))
        buttons.append(tk.Button(root, text="Mute", command=lambda: player.control('m')))
        buttons.append(tk.Button(root, text="Cycle Audio Channel", command=lambda: player.control('a')))
        buttons.append(tk.Button(root, text="Cycle Video Channel", command=lambda: player.control('v')))
        buttons.append(tk.Button(root, text="Cycle Subtitle Channel", command=lambda: player.control('t')))
        buttons.append(tk.Button(root, text="Cycle Program", command=lambda: player.control('c')))
        buttons.append(tk.Button(root, text="Cycle Video Filters", command=lambda: player.control('w')))
        buttons.append(tk.Button(root, text="Step Next Frame", command=lambda: player.control('s')))
        buttons.append(tk.Button(root, text="Seek Forward", command=lambda: player.control(Key.right)))
        buttons.append(tk.Button(root, text="Seek Backwards", command=lambda: player.control(Key.left)))
        buttons.append(tk.Button(root, text="Play / Pause", command=lambda: player.control(Key.space)))

        for i, button in enumerate(buttons):
            button.pack()
            # button.grid(row = i, column = 0, pady = 2)

        # Create a frame
        frame = tk.Frame(root, width=400, height=200)
        frame.pack_propagate(False)  # Prevents the frame from resizing to fit its contents

        # Create a text widget
        text = tk.Text(frame, wrap="word")  # 'word' wrapping style
        text.pack(side="left", fill="both", expand=True)

        # Create a scrollbar widget
        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side="right", fill="y")

        # Associate the scrollbar with the text widget
        text.config(yscrollcommand=scrollbar.set)

        # Set initial text
        text.insert("1.0", info)  # Inserts text at the beginning of the Text widget


        frame.pack()

        root.mainloop()


    def play(self, input_file = None):
        file_path = None
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
        elif input_file:
            file_path = input_file

        if file_path is None:
            print("This script requires a file to be dragged onto it or specified as an argument.")
            file_path = input("Please enter the file path (or drag and drop file): ")


        self.INPUT_FILE = file_path

        print(f"Playing File: {file_path}\n")
        print("WARNING: THIS IS ONLY FOR TESTING. PLAYBACK MAY STUTTER")
        self.ffplay.play(file_path)

        info = self.ffplay.probe(file_path)

        info = self.parse(info)

        self.control_popup(info)

    def control(self, key = None):
        if key is None:
            key = Key.space

        windows = gw.getWindowsWithTitle(self.INPUT_FILE)

        if windows:
            window = windows[0]
            window.activate()

            self.keyboard.press(key)
            self.keyboard.release(key)

        else:
            print(f"No window with title '{self.INPUT_FILE}' found.")


player = Player()

if __name__ == "__main__":
    player.play()