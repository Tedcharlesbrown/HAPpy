import tkinter as tk
from tkinter import filedialog
import ffmpeg

import os



def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename(title="Select a file")
    return filepath

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    folderpath = filedialog.askdirectory(title="Select a destination folder")
    return folderpath

def encode_to_hap(input_path, output_path):
    # Note: the exact FFmpeg command might vary based on the specific FFmpeg build and HAP variant.
    # The example below is for HAP Q encoding
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path, vcodec='hap', format='mov', compressor='snappy')
    ffmpeg.run(stream)

def main():
    input_path = select_file()
    if not input_path:
        print("No file selected. Exiting...")
        return

    destination_folder = select_folder()
    if not destination_folder:
        print("No destination folder selected. Exiting...")
        return

    base_name = os.path.basename(input_path)
    file_name, _ = os.path.splitext(base_name)
    output_path = f"{destination_folder}/{file_name}_HAP.mov"

    encode_to_hap(input_path, output_path)
    print(f"File saved to {output_path}")

if __name__ == "__main__":
    main()