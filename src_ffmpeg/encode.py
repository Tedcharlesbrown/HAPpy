import ffmpeg
import os

# Adjust these paths based on where you're keeping ffmpeg and ffprobe relative to your script
current_directory = os.path.dirname(os.path.abspath(__file__))
ffmpeg_bin = os.path.join(current_directory, 'FFMPEG')  # or 'ffmpeg/bin/ffmpeg' etc.
ffprobe_bin = os.path.join(current_directory, 'FFMPEG')  # or 'ffmpeg/bin/ffprobe' etc.

# Set the paths for ffmpeg-python
ffmpeg._run.DEFAULT_FFMPEG_PATH = ffmpeg_bin
ffmpeg._run.DEFAULT_FFPROBE_PATH = ffprobe_bin

def encode_to_hap(input_path, output_path):
    # Note: the exact FFmpeg command might vary based on the specific FFmpeg build and HAP variant.
    # The example below is for HAP encoding
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.output(stream, output_path, vcodec='hap', format='mov', compressor='snappy')
    ffmpeg.run(stream)

def encode_to_hap_half(input_path, output_path):
    # The example below is for HAP Q encoding with half resolution
    stream = ffmpeg.input(input_path)
    
    # Calculate dimensions and ensure they're divisible by 4
    width = 'floor(iw/2/4)*4'
    height = 'floor(ih/2/4)*4'

    #4/4
    #8/4

    # Scale video to the calculated dimensions
    scaled_stream = ffmpeg.filter(stream, 'scale', width, height)

    
    # Output the scaled stream with HAP codec settings
    out_stream = ffmpeg.output(scaled_stream, output_path, vcodec='hap', format='mov', compressor='snappy')
    
    ffmpeg.run(out_stream)