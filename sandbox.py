import subprocess
import os

def check_executable(executable_path):
    """Try to execute the given executable and return True if successful, else False."""
    try:
        # Running the executable with -version argument to get its version
        completed_process = subprocess.run([executable_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # If the return code is 0, it executed successfully
        if completed_process.returncode == 0:
            print(f"'{executable_path}' executed successfully!")
            print(completed_process.stdout.split('\n')[0])  # Printing the first line of the version info
            return True
        else:
            print(f"Error while executing '{executable_path}': {completed_process.stderr}")
            return False
            
    except FileNotFoundError:
        print(f"'{executable_path}' was not found!")
        return False
    except Exception as e:
        print(f"Unexpected error while executing '{executable_path}': {e}")
        return False

current_directory = os.path.dirname(os.path.abspath(__file__))
ffmpeg_folder = os.path.join(current_directory, 'FFMPEG')

ffmpeg_bin = os.path.join(ffmpeg_folder, 'ffmpeg.exe')
ffprobe_bin = os.path.join(ffmpeg_folder, 'ffprobe.exe')

# Check the executables
check_executable(ffmpeg_bin)
check_executable(ffprobe_bin)
