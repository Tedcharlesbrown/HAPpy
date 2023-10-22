import os
import threading
import time

from encode import Encoder

# ---------------------------------------------------------------------------- #
#                                    ENCODE                                    #
# ---------------------------------------------------------------------------- #



def on_encode_click(self, selected):
    """Handles the encode button click event."""
    self.elapsed_files = 1
    selected_items = self.tree.selection()
    
    if not selected:
        self.tree.selection_remove(selected_items)

    all_files_to_encode = []

    # If nothing is selected, get all children of the root folder
    if not selected_items:
        root_items = self.tree.get_children()
        for root in root_items:
            all_files_to_encode.extend(self.gather_files_for_encode(root))
    else:
        for item in selected_items:
            all_files_to_encode.extend(self.gather_files_for_encode(item))

    # Count the total files to encode
    self.total_files = len(all_files_to_encode)
    print(f"Total number of files to encode: {self.total_files}")

    #TODO gather checkbox values
    print(self.var_destination_same_as_source.get())
    print(self.var_create_hap_folder_at_source.get())
    print(self.var_append_hap_to_file_name.get())

    # Now you can send them to the encoder
    for file_path in all_files_to_encode:
        # print(file_path, self.destination_path)
        self.send_to_encoder(file_path)

def send_to_encoder(self, file_path):
    # Extract file name and its immediate parent
    file_name = os.path.basename(file_path)
    # path_parent = os.path.basename(os.path.dirname(file_path))

    # # Decide the destination folder
    # if not self.destination_path:
    #     # Identify the base directory 
    #     base_path = os.path.dirname(file_path)
    #     while os.path.basename(base_path) != self.parent_folder and base_path:
    #         base_path = os.path.dirname(base_path)
    #     destination_path = os.path.join(base_path, "HAP")
    #     # destination_path = base_path
    # else:
    #     destination_path = self.destination_path

    # # Preserve the subdirectory structure if the immediate parent of the file is not self.parent_folder
    # if path_parent != self.parent_folder:
    #     destination_path = os.path.join(destination_path, path_parent)

    # # Construct the final path where the file will be placed/encoded
    # # final_path = os.path.splitext(os.path.join(destination_path, file_name))[0]

    # final_path = os.path.join(os.path.dirname(file_path), file_name)

    final_path = os.path.join(os.path.dirname(file_path), file_name)

    if self.destination_path:
        # print("DESTINATION PATH EXISTS")
        final_path = os.path.join((self.destination_path), file_name)

    # print(f"DESTINATION FOLDER = {self.destination_path}")
    print(f"FROM ENCODER: {file_path} --> {final_path}")

    self.encode_queue.put((file_path, final_path))

    # You can start the encoder thread (if it's not already running):
    if not hasattr(self, "encoder_thread") or not self.encoder_thread.is_alive():
        self.encoder_thread = threading.Thread(target=self.encoder_worker)
        self.encoder_thread.start()

    #TODO Create HAP folder in parent folder
def append_to_hap_folder(self, file_path):
    pass

def encoder_worker(self):
    while not self.encode_queue.empty():
        file_path, final_path = self.encode_queue.get()
        self.run_encoder(file_path, final_path)

def run_encoder(self, file_path, final_path):
    # Force Reset progress bar to 0
    if self.console_log_progress:
        self.console_log_progress(0.0)
    time.sleep(0.25)
    self.root.after(0, self.update_progress_text, f"({self.elapsed_files}/{self.total_files}) : {os.path.basename(file_path)}")
    result = self.encoder.encode_to_hap(file_path, final_path, mode="scale", callback=self.console_log_progress)  # <-- Added the callback parameter here

    if result:
        time.sleep(0.25)
        with self.encode_lock:
            print(f"ELAPSED: {self.elapsed_files}")
            self.elapsed_files += 1
