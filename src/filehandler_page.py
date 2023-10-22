import os
from tkinter import filedialog
from tkinterdnd2 import DND_FILES, Tk

# ---------------------------------------------------------------------------- #
#                                 INPUT METHODS                                #
# ---------------------------------------------------------------------------- #

# --------------------------- FILE OR FOLDER DIALOG -------------------------- #
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

# ----------------------------- IMPORT FILE TREE ----------------------------- #
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
        if folder_path.startswith("{") and folder_path.endswith("}"): # Copy pasted files have curly braces around them
            folder_path = folder_path[1:-1]
        filename = os.path.basename(folder_path)
        found_acceptable_extension = any(filename.endswith(container) for container in self.acceptable_containers)

        if found_acceptable_extension:
            self.console.log(f"Displaying {folder_path} to the file tree", "FILE")
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
            self.console.log(f"Populating {entry_path} to the file tree", "FILE")
            self.tree.insert(parent, "end", text=filename, values=(entry_path,))

    # ------------------------ OPEN DIRECTORES IN TREE ----------------------- #
    check_file_tree(self)

def display_destination_folder(self, folder_path):
    """Displays the selected destination folder."""
    if folder_path.startswith("{") and folder_path.endswith("}"): # Copy pasted files have curly braces around them
            folder_path = folder_path[1:-1]
    self.destination_label.config(text=folder_path)  # Update the label text with the new destination
    self.console.log(f"Destination folder set to {folder_path}", "DESTINATION")
    self.var_destination_same_as_source.set(False)
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

def clear_selection(self):
    """Deselects the currently selected items in the tree."""
    selected_items = self.tree.selection()
    for item in selected_items:
        self.tree.selection_remove(item)

def remove_file_from_tree(self):
    """Removes selected files or directories from the file tree in the Treeview. 
       If no items are selected, remove all files and empty directories."""

    def delete_items_recursive(items):
        """Recursively deletes files and checks if a directory is empty."""
        for item in items:
            if self.tree.item(item)["values"]:  # Check if the item is a file
                self.console.log(f"Removing {self.tree.item(item, 'text')} from the file tree", "FILE")
                self.tree.delete(item)
            else:
                # Recursively delete files and sub-directories within this directory
                delete_items_recursive(self.tree.get_children(item))
                # Check if the directory is now empty and delete it if so
                if not self.tree.get_children(item):
                    self.tree.delete(item)

    selected_items = self.tree.selection()
    
    # If items are selected
    if selected_items:
        delete_items_recursive(selected_items)
    # If no items are selected, remove all files from the tree
    else:
        delete_items_recursive(self.tree.get_children())

    check_file_tree(self)


def check_file_tree(self):
    """Opens each directory in the Treeview. If a directory has no children, it's removed."""

    def check_items_recursive(items):
        """Recursively opens directories and checks if a directory is empty."""
        for item in items:
            # If the item is a directory
            if not self.tree.item(item)["values"]:
                self.tree.item(item, open=True)  # Open the directory
                # Recursively check children
                check_items_recursive(self.tree.get_children(item))
                # If the directory is now empty after checking children, delete it
                if not self.tree.get_children(item):
                    self.tree.delete(item)

    # Start the check from the top level of the tree
    check_items_recursive(self.tree.get_children())