import subprocess

def encode_to_hap(input_file, output_file, ffmpeg_bin_path="ffmpeg"):
    """
    Encode a video to the HAP codec using subprocess to call ffmpeg directly.

    Parameters:
    - input_file: Path to the input video file.
    - output_file: Path to the output HAP encoded video file.
    - ffmpeg_bin_path: Path to the ffmpeg binary.
    """
    
    # Create the ffmpeg command
    cmd = [
        ffmpeg_bin_path,
        '-i', input_file,
        '-vcodec', 'hap',
        '-y',  # Overwrite output file if it exists
        output_file
    ]
    
    # Run the command
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    input_path = r"C:\Users\TedCh\OneDrive\Desktop\test\input.png"
    output_path = r"C:\Users\TedCh\OneDrive\Desktop\test\output.mov"
    ffmpeg_binary = r"C:\Users\TedCh\OneDrive\Documents\GitHub\HAPpy\FFMPEG\ffmpeg.exe"

    encode_to_hap(input_path, output_path, ffmpeg_binary)
