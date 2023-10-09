import os

from src_tkinter.handle_files import select_file
from src_tkinter.handle_files import select_folder

from src_ffmpeg.encode import encode_to_hap

def menu_select_input():
    input_path = select_file()
    if not input_path:
        print("No file selected. Exiting...")
        return
    return input_path

def menu_select_input_folder():
    folder_path = select_folder()
    if not folder_path:
        print("No folder selected. Exiting...")
        return
    # List all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Optionally, you can filter for specific file types (e.g., only .mov files)
    # files = [f for f in files if f.endswith('.mov')]

    # Return full paths of all files
    return [os.path.join(folder_path, f) for f in files]

def menu_select_destination():
    destination_path = select_folder()
    if not destination_path:
        print("No destination folder selected. Exiting...")
        return
    return destination_path

def menu_select_source_file():
    input_path = menu_select_input()
    destination_path = menu_select_destination()

    base_name = os.path.basename(input_path)
    file_name, _ = os.path.splitext(base_name)
    output_path = f"{destination_path}/{file_name}_HAP.mov"

    encode_to_hap(input_path, output_path)
    print(f"File saved to {output_path}")

def menu_select_source_folder():
    input_paths = menu_select_input_folder()
    destination_folder = menu_select_destination()

    # Iterate over each file in the selected folder
    for input_path in input_paths:
        base_name = os.path.basename(input_path)
        file_name, _ = os.path.splitext(base_name)
        output_path = f"{destination_folder}/{file_name}_HAP.mov"
        
        encode_to_hap(input_path, output_path)
        print(f"File saved to {output_path}")


def main():
    menu_select_source_folder()
    

if __name__ == "__main__":
    main()
