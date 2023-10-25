import os
import subprocess
import re
import ffmpeg  # ffmpeg-python

ffmpeg_bin = ("../FFMPEG/ffmpeg.exe")
ffprobe_bin = ("../FFMPEG/ffprobe.exe")
cmd = ""

def init():
    ffmpeg_version = None
    ffprobe_version = None

    ffmpeg._run.DEFAULT_FFMPEG_PATH = ffmpeg_bin
    ffmpeg._run.DEFAULT_FFPROBE_PATH = ffprobe_bin  



def get_video_dimensions(input_path):
    cmd = [ffprobe_bin, '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_path]
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    width, height = map(int, output.split(','))
    return width, height


@staticmethod
def round_up_to_nearest_four(n):
    return (n + 3) & ~3  # Rounds up to the nearest multiple of 4

def encode(input_path, output_path, mode="scale"):
    width, height = get_video_dimensions(input_path)
    original_aspect_ratio = width / height
    invalid_width = False
    invalid_height = False

    #CHECK IF WIDTH AND HEIGHT ARE DIVISIBLE BY 4
    # if width%4 != 0:
    #     invalid_width = True
    #     width = round_up_to_nearest_four(width) 
    #     print("Width is not divisible by 4")

    # if height%4 != 0:
    #     invalid_height = True
    #     height = round_up_to_nearest_four(height)
    #     print("Height is not divisible by 4")

    #TODO MOVE THIS TO APP
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Create the ffmpeg command
    cmd = [ffmpeg_bin,'-i', input_path]

    width = 1001
    height = 1001

    if mode == "pad":
        cmd.extend(['-vf', f'pad={width}:{height}:0:0:green'])
    elif mode == "stretch":
        cmd.extend(['-vf', f'scale={width}:{height}'])
    elif mode == "scale-new":
        attempts = 0
        max_attempts = 100

        while (width % 4 != 0 or height % 4 != 0) and attempts < max_attempts:
            print(attempts, height, width)

            if width % 4 != 0:
                width = round_up_to_nearest_four(width)
                height = int(width / original_aspect_ratio)
            if height % 4 != 0:
                height = round_up_to_nearest_four(height)
                width = int(height * original_aspect_ratio)
        
            attempts += 1


        if attempts == max_attempts:
            print("Unable to adjust dimensions while maintaining aspect ratio after 100 attempts.")
            return
        
        print(f"FOUND IN {attempts}", width, height, original_aspect_ratio, width / height)
        cmd.extend(['-vf', f'scale={width}:{height}'])
        
    elif mode == "scale-old":
        if invalid_width and invalid_height:
            cmd.extend(['-vf', f'scale={width}:{height}'])
        elif invalid_width:
            cmd.extend(['-vf', f'scale={width}:-1'])
        elif invalid_height:
            cmd.extend(['-vf', f'scale=-1:{height}'])
        else:
            cmd.extend(['-vf', f'scale=-1:-1'])
    else:
        raise ValueError("Invalid mode.")
    

    cmd.extend([
        '-c:v', 'png',
        # '-format', codec, # hap, hap_alpha, hap_q
        '-y',
        # os.path.splitext(output_path)[0] + "_HAP.mov"
        output_path
    ])

    print(" ".join(cmd))
    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

init()

path = r"C:\Users\TedCh\OneDrive\Desktop\HAPPY TEST\bad_resolutions"
input_path = os.path.join(path, "invalid_height.png")
output_path = os.path.join(path, "test-new.png")

encode(input_path, output_path, "scale-new")