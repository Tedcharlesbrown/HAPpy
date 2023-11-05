import sys
import json
from encode import FFMPEG

player = FFMPEG()


if len(sys.argv) > 1:
    file_path = sys.argv[1]
    print(f"Playing File: {file_path}\n")
    player.play(file_path)

    info = player.probe(file_path)

    print(json.dumps(info, indent=3))


    # print(f"Codec: {info['streams'][0]['codec_name']}")
    # print(f"Codec Long Name: {info['streams'][0]['codec_long_name']}")
    # print(f"Codec Tag: {info['streams'][0]['codec_tag_string']}")
    # # print("\n")
    # print(f"Resolution: {info['streams'][0]['width']}x{info['streams'][0]['height']}")
    # print(f"Aspect Ratio: {info['streams'][0]['display_aspect_ratio']}")
    # # print("\n")
    # print(f"Frame Rate: {info['streams'][0]['r_frame_rate'][:-2]}")
    # print(f"Duration: {info['streams'][0]['duration']}")
    # print(f"Timecode: {info['streams'][0]['tags']['timecode']}")
    # # print("\n")
    # print(f"Color Primaries: {info['streams'][0]['color_primaries']}")
    # print(f"Color Space: {info['streams'][0]['color_space']}")
    # print(f"Pixel Format: {info['streams'][0]['pix_fmt']}")
    # print(f"Field Order: {info['streams'][0]['field_order']}")
    # print("\n")

else:
    print("This script requires a file to be dragged onto it.")