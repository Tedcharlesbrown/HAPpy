import ffmpeg  # ffmpeg-python
import os
import subprocess
import re


class Encoder:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.ffmpeg_bin = os.path.join(current_directory, 'FFMPEG')
        self.ffprobe_bin = os.path.join(current_directory, 'FFMPEG')

        # Set the paths for ffmpeg-python
        ffmpeg._run.DEFAULT_FFMPEG_PATH = self.ffmpeg_bin
        ffmpeg._run.DEFAULT_FFPROBE_PATH = self.ffprobe_bin 

    @staticmethod
    def get_video_dimensions(input_path):
        probe = ffmpeg.probe(input_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        return int(video_stream['width']), int(video_stream['height'])

    @staticmethod
    def round_up_to_nearest_four(n):
        return (n + 3) & ~3  # Rounds up to the nearest multiple of 4

    def encode_to_hap(self, input_path, output_path, mode="pad", callback=None):
        width, height = self.get_video_dimensions(input_path)

        new_width = self.round_up_to_nearest_four(width)
        new_height = self.round_up_to_nearest_four(height)

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        stream = ffmpeg.input(input_path)

        if mode == "pad":
            pad_right = new_width - width
            pad_bottom = new_height - height
            stream = ffmpeg.filter(stream, 'pad', new_width, new_height, 0, 0, color="black")
        elif mode == "scale":
            stream = ffmpeg.filter(stream, 'scale', new_width, new_height)
        else:
            raise ValueError("Invalid mode. Please use 'pad' or 'scale'.")

        stream = ffmpeg.output(stream, output_path + ".mov", vcodec='hap', format='mov', compressor='snappy')
        
        cmd = ffmpeg.compile(stream, overwrite_output=True)
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)

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

        return_code = process.wait()
        # After FFmpeg finishes, make sure you set the progress to 100%.
        if callback:
            callback(100.0)


