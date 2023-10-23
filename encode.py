import os
import subprocess
import re
import ffmpeg  # ffmpeg-python

from autopytoexe_path import resource_path

class Encoder:
    def __init__(self):
        ffmpeg_folder = resource_path('FFMPEG')

        self.ffmpeg_bin = os.path.join(ffmpeg_folder, 'ffmpeg.exe')
        self.ffprobe_bin = os.path.join(ffmpeg_folder, 'ffprobe.exe')
        self.ffmpeg_version = None
        self.ffprobe_version = None

        # Check if the specified ffmpeg.exe file exists
        if os.path.exists(ffmpeg_folder):
            try:
                self.ffmpeg_version = subprocess.run([self.ffmpeg_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.ffmpeg_version = self.ffmpeg_version.stdout.decode('utf-8').splitlines()[0]
                # print(self.ffmpeg_version)
            except subprocess.CalledProcessError as e:
                print("ERROR")
            try:
                self.ffprobe_version = subprocess.run([self.ffprobe_bin, '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.ffprobe_version = self.ffprobe_version.stdout.decode('utf-8').splitlines()[0]
                # print(self.ffprobe_version)
            except subprocess.CalledProcessError as e:
                print("ERROR")

        ffmpeg._run.DEFAULT_FFMPEG_PATH = self.ffmpeg_bin
        ffmpeg._run.DEFAULT_FFPROBE_PATH = self.ffprobe_bin     
    
    def __str__(self):
        return f"FFmpeg version: {self.ffmpeg_version}\nFFprobe version: {self.ffprobe_version}"
    
    def get_version(self, exe="ffmpeg"):
        if exe == "ffmpeg":
            return self.ffmpeg_version
        elif exe == "ffprobe":
            return self.ffprobe_version
        else:
            raise ValueError("Invalid argument. Please use 'ffmpeg' or 'ffprobe'.")

    @staticmethod
    def get_video_dimensions(self, input_path):
        cmd = [self.ffprobe_bin, '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_path]
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        width, height = map(int, output.split(','))
        return width, height


    @staticmethod
    def round_up_to_nearest_four(n):
        return (n + 3) & ~3  # Rounds up to the nearest multiple of 4

    def encode_to_hap(self, input_path, output_path, codec="hap_alpha", mode="scale", callback=None):
        width, height = self.get_video_dimensions(self, input_path)

        new_width = self.round_up_to_nearest_four(width)
        new_height = self.round_up_to_nearest_four(height)

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        # Create the ffmpeg command
        cmd = [
            self.ffmpeg_bin,
            '-i', input_path
        ]

        if mode == "pad":
            cmd.extend(['-vf', f'pad={new_width}:{new_height}:0:0:black'])
        elif mode == "scale":
            cmd.extend(['-vf', f'scale={new_width}:{new_height}'])
        else:
            raise ValueError("Invalid mode. Please use 'pad' or 'scale'.")

        cmd.extend([
            '-c:v', 'hap',
            '-format', codec, # hap, hap_alpha, hap_q
            '-y',
            # os.path.splitext(output_path)[0] + "_HAP.mov"
            output_path + ".mov"
        ])

        print(" ".join(cmd))
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

        # stdout, stderr = process.communicate()
        # if process.returncode != 0:
        #     print(f"FFmpeg failed with error: {stderr}")
        # else:
        #     print(stdout)

        duration_pattern = re.compile(r"Duration: (\d+:\d+:\d+\.\d+)")
        progress_pattern = re.compile(r"time=(\d+:\d+:\d+\.\d+)")

        duration = None
        for line in iter(process.stderr.readline, ""):
            if duration is None:
                match = duration_pattern.search(line)
                if match:
                    duration = sum(float(x) * 60 ** i for i, x in enumerate(reversed(match.group(1).split(":"))))
            match = progress_pattern.search(line)
            if match:
                progress_time = sum(float(x) * 60 ** i for i, x in enumerate(reversed(match.group(1).split(":"))))
                progress_percentage = (progress_time / duration) * 100 if duration else 0
                if callback:
                    callback(progress_percentage)

        # return_code = process.wait()
        # After FFmpeg finishes, make sure you set the progress to 100%.
        if callback:
            callback(100.0)
            return cmd, True
