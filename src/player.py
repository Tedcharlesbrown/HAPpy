import sys
import json
from encode import FFMPEG

player = FFMPEG()


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
    player.play(file_path)

    info = player.probe(file_path)

    print(json.dumps(info, indent=3))

play()