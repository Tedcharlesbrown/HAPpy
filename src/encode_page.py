import os
import threading
import time

# from encode import Encoder

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
    self.console.log(f"Total number of files to encode: {self.total_files}", "ENCODE")

    # Now you can send them to the encoder
    for file_path in all_files_to_encode:
        self.send_to_encoder(file_path)

def send_to_encoder(self, file_path):
    # get parent folder name
    self.parent_folder = os.path.dirname(file_path)
    self.file = os.path.basename(file_path)
    self.file = os.path.splitext(self.file)[0]

    def set_final_path():
        # -------------------------- APPEND HAP TO FILE NAME ------------------------- #
        if self.var_append_hap_to_file_name.get():
            if self.file.lower().find("_v") > 0:
                file_prefix = self.file[:self.file.lower().rfind("_v")]
                file_version = self.file[self.file.lower().rfind("_v"):]
                self.file = file_prefix + "_HAP" + file_version
            else:
                self.file += "_HAP"
        # ---------------------------- SOURCE DESTINATION ---------------------------- #
        if self.var_destination_same_as_source.get():
            if self.var_create_hap_folder_at_source.get():
                # APPEND HAP TO PARENT FOLDER
                self.parent_folder = os.path.join(self.parent_folder, "HAP")
                final_path = os.path.join(self.parent_folder, self.file)
            else:
                final_path = os.path.join(self.parent_folder, self.file)
        else:
            final_path = os.path.join(self.destination_path, self.file)

        return final_path
    
    def check_for_overwrite(path):
        current_file = os.path.basename(path) + ".mov"
        directory = os.path.dirname(path)
        print(directory)
        for file in os.listdir(directory):
            if current_file == file:
                if not self.overwrite_all_files:
                    self.console.log(f"File already exists: {current_file}", "ENCODE")
                    result = self.trigger_overwrite_popup()
                    if result == "ALL":  # OVERWRITE ALL
                        self.console.log(f"Overwriting all files", "ENCODE")
                        self.overwrite_all_files = True
                        # return True
                    elif result == "YES":  # OVERWRITE
                        self.console.log(f"Overwriting file", "ENCODE")
                        # return True
                    elif result == "SKIP":  # DONT OVERWRITE
                        self.console.log(f"Skipping file", "ENCODE")
                        return False

                # IF DESTINATION SAME AS SOURCE, NOT APPENDING HAP, PRESERVE ORIGINAL FILE
                if self.var_destination_same_as_source.get() and not self.var_append_hap_to_file_name.get() and not self.destination_path:
                    current_file = os.path.splitext(current_file)[0]
                    if current_file.find("_v") > 0:
                        file_prefix = current_file[:current_file.lower().rfind("_v")]
                        file_version = current_file[current_file.lower().rfind("_v")+2:]
                        file_version = int(file_version) + 1
                        current_file = file_prefix + "_v" + str(file_version)
                    else:
                        current_file = current_file + "_v1"

                    self.final_path = os.path.join(self.parent_folder, current_file)

        return True  # return True if no matching file found in directory

    self.final_path = set_final_path()
    if (check_for_overwrite(self.final_path)):
        self.console.log(f"Sending {file_path} to the encoder", "ENCODE")

        self.encode_queue.put((file_path, self.final_path))

        # Start the encoder thread (if it's not already running):
        if not hasattr(self, "encoder_thread") or not self.encoder_thread.is_alive():
            self.encoder_thread = threading.Thread(target=self.encoder_worker)
            self.encoder_thread.start()

    #TODO Create HAP folder in parent folder
def append_to_hap_folder(self, file_path):
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
    pass

def encoder_worker(self):
    while not self.encode_queue.empty():
        file_path, final_path = self.encode_queue.get()
        self.run_encoder(file_path, final_path)

def run_encoder(self, file_path, final_path):
    
    def update_progress_text(text):
        self.root.after(0, lambda: self.update_progress_text(text))

    # Force Reset progress bar to 0
    if self.console_log_progress:
        self.console_log_progress(0.0)
    time.sleep(0.25)
    # self.root.after(0, self.update_progress_text, f"({self.elapsed_files}/{self.total_files}) : {os.path.basename(file_path)}")
    update_progress_text(f"({self.elapsed_files}/{self.total_files}) : {os.path.basename(file_path)}")
    result = self.encoder.encode_to_hap(file_path, final_path, mode="scale", callback=self.console_log_progress)

    if result is True:
        time.sleep(0.25)
        with self.encode_lock:
            self.elapsed_files += 1

            if self.elapsed_files > self.total_files:
                time.sleep(0.5)
                update_progress_text("Encoding complete!")
                self.console.log("Encoding complete!", "ENCODE")
                self.overwrite_all_files = False
                # time.sleep(2)
                # update_progress_text("Not Currently Encoding")
                # self.progress["value"] = 0

