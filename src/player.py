'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

import sys
import json
from encode import FFMPEG

import time
from pynput.keyboard import Key, Controller
import pygetwindow as gw

keyboard = Controller()



player = FFMPEG()

def parse(info):
    # print(json.dumps(info, indent=3))
    # print(info['streams'])
    for stream in info['streams']:
        try:
            if stream['codec_type'] == "video" or stream['codec_type'] == "audio":
                print(f"\nCODEC TYPE: {stream['codec_type']}")
                print(f"CODEC NAME: {stream['codec_name']}")
                print(f"CODEC LONG NAME: {stream['codec_long_name']}")
                print(f"CODEC TAG: {stream['codec_tag_string']}")
            # ----------------------------------- VIDEO ---------------------------------- #
            if stream['codec_type'] == "video":
                print(f"DIMENSIONS: {stream['width']}x{stream['height']}")
                print(f"PIXEL FORMAT: {stream['pix_fmt']}")
                print(f"BITRATE: {stream['bit_rate']}")
                frame_rate = stream['r_frame_rate'].split('/')
                frame_rate = int(frame_rate[0]) / int(frame_rate[1])
                print(f"FRAME RATE: {frame_rate}")
                print(f"COLOR TRANSFER: {stream['color_transfer']}")
                print(f"COLOR SPACE: {stream['color_space']}")
                print(f"FIELD ORDER: {stream['field_order']}")
                print(f"DURATION: {stream['duration']}")
            # ----------------------------------- AUDIO ---------------------------------- #
            if stream['codec_type'] == "audio":
                print(f"CHANNELS: {stream['channels']}")
                print(f"SAMPLE RATE: {stream['sample_rate']}")
                print(f"CHANNEL LAYOUT: {stream['channel_layout']}")
                print(f"BITRATE: {stream['bit_rate']}")
                print(f"DURATION: {stream['duration']}")

        except:
            pass


def play(input_file = None):
    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    elif input_file:
        file_path = input_file

    if file_path is None:
        print("This script requires a file to be dragged onto it or specified as an argument.")
        file_path = input("Please enter the file path (or drag and drop file): ")

    print(f"Playing File: {file_path}\n")
    print("WARNING: THIS IS ONLY FOR TESTING. PLAYBACK MAY STUTTER")
    player.play(file_path)

    # control(key='w',file_path=file_path)

    info = player.probe(file_path)

    info = parse(info)

    


def control(key = None, file_path = None):
    if key is None:
        key = Key.space

    time.sleep(0.25)

    windows = gw.getWindowsWithTitle(file_path)

    if windows:
        window = windows[0]
        window.activate()
        time.sleep(0.25)

        keyboard.press(key)
        keyboard.release(key)

    else:
        print(f"No window with title '{file_path}' found.")



if __name__ == "__main__":
    play()