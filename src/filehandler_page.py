import os
from tkinter import ttk, filedialog, PhotoImage, font


def open_file_or_folder_dialog(self, button, event=None):
    """Opens a file or folder dialog based on which label was clicked."""
    paths = ""
    if button == "INPUT_FILE":
        paths = filedialog.askopenfilenames()
    elif button == "INPUT_FOLDER":
        paths = filedialog.askdirectory()
    elif button == "DESTINATION_FOLDER":
        self.display_destination_folder(filedialog.askdirectory())

    if paths:
        for path in paths:
            self.display_input_tree(path)  # Send each individual file path to be displayed

def display_input_tree(self, folder_path):
    """Displays the file tree of the specified folder in the Treeview."""
    # -------------------- REMOVE INITIAL PROMPT ------------------- #
    if self.tree.exists(self.drag_prompt_id):
        self.tree.delete(self.drag_prompt_id)


    # ----------------- CHECK IF PATH EXISTS ----------------- #
    for item in self.tree.get_children():
        item_value = self.tree.item(item, 'values')
        if folder_path in item_value:
            print(f"Path {folder_path} already exists in the tree. Skipping...") #TODO This only works with single files
            return

    # -------------------------- CHECK IF FILE OR FOLDER ------------------------- #
    # If the path is a directory, create a top-level parent node for the directory
    if os.path.isdir(folder_path):
        root_item = self.tree.insert("", "end", text=os.path.basename(folder_path))
        self.populate_file_tree(root_item, folder_path)

    else:  # If it's a single file
        filename = os.path.basename(folder_path).replace("}", "")
        found_acceptable_extension = any(filename.endswith(container) for container in self.acceptable_containers)

        if found_acceptable_extension:
            self.tree.insert("", "end", text=filename, values=(folder_path,))
        else:
            print(f"FILE EXTENSION ERROR: {filename}")
            return

def populate_file_tree(self, parent, folder_path):
    """Helper method to populate the Treeview with the file structure."""

    # ------------------------- LOOP THROUGH DIRECTORIES ------------------------- #
    for entry in sorted(os.listdir(folder_path)):
        entry_path = os.path.join(folder_path, entry)

        # ------------------------------- SUB DIRECTORY ------------------------------ #
        if os.path.isdir(entry_path):
            child_item = self.tree.insert(parent, "end", text=entry)  # Create a parent node for sub-directory
            self.tree.item(child_item, open=True)  # Open the tree node by default
            self.populate_file_tree(child_item, entry_path)  # Recurse into the sub-directory
    
    # ------------------------------- HANDLE FILES ------------------------------- #
    for entry in sorted(os.listdir(folder_path)):
        entry_path = os.path.join(folder_path, entry)
        filename = os.path.basename(entry_path)
        if any(filename.endswith(container) for container in self.acceptable_containers): # only add acceptable exstensions
            self.tree.insert(parent, "end", text=filename, values=(entry_path,))

    # ------------------------ OPEN DIRECTORES IN TREE ----------------------- #
    for item in self.tree.get_children():
        self.tree.item(item, open=True)

def display_destination_folder(self, folder_path):
    """Displays the selected destination folder."""
    self.destination_label.config(text=folder_path)  # Update the label text with the new destination
    self.destination_path = folder_path  

def gather_files_for_encode(self, item_id):
    """Recursively gathers all file paths from a given item (and its children if it's a directory)."""
    item_data = self.tree.item(item_id)
    file_paths = []

    if item_data["values"]:  # It's a file
        file_paths.append(item_data["values"][0])
    else:  # It's a directory
        for child_id in self.tree.get_children(item_id):
            file_paths.extend(self.gather_files_for_encode(child_id))

    return file_paths