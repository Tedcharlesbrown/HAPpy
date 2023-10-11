import os
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import queue
import time

from encode import encode_to_hap


class App:
    def __init__(self, root):
        self.encode_queue = queue.Queue()
        self.encode_lock = threading.Lock()
        self.root = root
        self.codec_option = tk.StringVar()  # Move this line here
        self.configure_styles()
        self.setup_ui()
        self.acceptable_containers = [".mkv", ".mp4", ".mov", ".asf", ".avi", ".mxf", ".m2p", ".ps", ".ts", ".m2ts", ".mts", ".vob", ".evo", ".3gp", ".3g2", ".f4v", ".flv", ".ogv", ".ogx", ".webm", ".rmvb", ".divx", ".png", ".jpg", ".jpeg", ".tiff", ".svg"]
        self.destination_path = ""
        self.parent_folder = ""
        self.elapsed_files = 1
        self.total_files = 0
        self.job_is_complete = False

    def setup_ui(self):
        # Source Drag and Drop Area
        self.setup_drop_area(x=20, y=80, width=170, height=60, label_text="Click here to select a file", func=self.open_file_dialog)
        self.setup_drop_area(x=200, y=80, width=170, height=60, label_text="Click here to select a folder", func=self.open_folder_dialog)

        # Treeview for displaying the file structure of the source
        self.setup_treeview(x=20, y=150, width=350, height=300)

        # Destination Drag and Drop Area
        # self.setup_drop_area(x=20, y=470, width=350, height=60, label_text="Click here to select a destination", func=self.open_folder_dialog)
        self.setup_drop_area(x=430, y=80, width=350, height=60, label_text="Click here to select a destination", func=self.open_folder_dialog)

        # Frame to display the selected destination folder
        self.destination_label = ttk.Label(self.root, text="Drop destination folder here", wraplength=300, style="Destination.TLabel")
        # self.destination_label.place(x=20, y=540, width=350, height=40)
        self.destination_label.place(x=430, y=80+70, width=350, height=40)
        self.destination_label.drop_target_register(DND_FILES)
        self.destination_label.dnd_bind('<<Drop>>', self.drop)
        self.destination_label.bind('<Button-1>', self.open_folder_dialog)

        # Checkboxes
        self.setup_checkboxes()

        # self.setup_dropdown()

        self.setup_progressbar()

        # Encode Button
        # button_encode_selected = ttk.Button(self.root, text="Encode Selected", style="TButton", command=self.on_encode_click)
        button_encode_selected = ttk.Button(self.root, text="Encode Selected", style="encode_selected.TButton", command=lambda: self.on_encode_click(True))
        button_encode_selected.place(x=425, y=470)
        button_encode_all = ttk.Button(self.root, text="Encode ALL", style="encode_all.TButton", command=lambda: self.on_encode_click(False))
        button_encode_all.place(x=609, y=470)

    

    def configure_styles(self):
        self.style_progressbar_background = '#333333'
        # Dark mode styling
        style = ttk.Style()
        self.style = ttk.Style(root)

        style.theme_use("default")
        style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")

        self.style_button_background = "#555555"
        self.style_button_foreground = "#FFFFFF"
        self.style_button_pressed = "#444444"
        self.style_button_active = "#5E5E5E"

        style.configure("encode_selected.TButton", background=self.style_button_background, foreground=self.style_button_foreground, relief="raised", padding=(37.5,20))
        style.map("encode_selected.TButton", background=[('pressed', self.style_button_pressed), ('active', self.style_button_active)])
        style.configure("encode_all.TButton", background=self.style_button_background, foreground=self.style_button_foreground, relief="raised", padding=(50,20))
        style.map("encode_all.TButton", background=[('pressed', self.style_button_pressed), ('active', self.style_button_active)])

        style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
        style.configure("Treeview.Heading", background="#555555", foreground="#FFFFFF")
        
        # Configure the styling for the destination label
        style.configure("Destination.TLabel", 
                        background="#333333",    # Background color
                        foreground="#FFFFFF",    # Foreground color (text color)
                        padding=10,              # Padding around the text
                        relief="sunken")         # Border type
        
        style.configure("TCheckbutton", background="#2E2E2E", foreground="#FFFFFF", relief="flat")
        style.map("TCheckbutton", background=[('active', '#2E2E2E')], indicatorcolor=[("selected", "#555555")], indicatorrelief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure("TCheckbutton", font=100)  # Adjust size as needed
        
        style.configure("TCombobox", 
                        fieldbackground="#333333",    # Combobox's main color
                        background="#555555",         # Arrow button color
                        foreground="#FFFFFF",         # Text color
                        arrowcolor="#FFFFFF",         # Arrow color
                        borderwidth=0,                # Border width
                        padding=5)                    # Padding around text
        
        style.map("TCombobox", 
                fieldbackground=[('readonly', "#000000")], 
                selectbackground=[('readonly', "#555555")],
                selectforeground=[('readonly', "#555555")])

        # Configure style for the button
        style.configure("Dark.TButton", background="#555555", foreground="#FFFFFF", font=("Arial", 14), relief="raised", padding=(20, 10))
        style.map("Dark.TButton", background=[('pressed', '#333333'), ('active', '#444444')])

        style.layout('text.Horizontal.TProgressbar', 
                         [('Horizontal.Progressbar.trough',
                           {'children': [('Horizontal.Progressbar.pbar',
                                          {'side': 'left', 'sticky': 'ns'})],
                            'sticky': 'nswe'}), 
                          ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
        style.configure('text.Horizontal.TProgressbar', relief='sunken', text='Not Currently Encoding', foreground="white", anchor='center', troughcolor=self.style_progressbar_background, background='green')

    def setup_drop_area(self, x, y, width, height, label_text, func):
        drop_area = tk.Label(self.root, bg='#555555', fg='#FFFFFF', relief="raised", text=label_text)
        drop_area.place(x=x, y=y, width=width, height=height)
        drop_area.drop_target_register(DND_FILES)
        drop_area.dnd_bind('<<Drop>>', self.drop)
        drop_area.bind('<Button-1>', func)

    def drop_for_source(self, event):
        self.display_file_tree(event.data)

    def drop_for_destination(self, event):
        self.display_destination_folder(event.data)

    def setup_treeview(self, x, y, width, height):
        self.tree = ttk.Treeview(self.root)
        self.tree.place(x=x, y=y, width=width, height=height)
        self.tree['show'] = 'tree'
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self.drop_to_treeview)  # Bind the Drop event
        self.drag_prompt_id = self.tree.insert("", "end", text="Drop source file / folder here")

        # self.tree.insert("", "end", text="Drop source file / folder here")

    def drop_to_treeview(self, event):
        widget_type = event.widget.winfo_class()
        if widget_type == "Treeview":
            self.display_file_tree(event.data)

    def setup_checkboxes(self):
        var_destination_match_source = tk.IntVar()
        var_append_hap = tk.IntVar()
        var_create_proxys = tk.IntVar()
        var_create_proxys_only = tk.IntVar()
        var_create_thumbnails = tk.IntVar()
        var_create_thumbnails_only = tk.IntVar()
        var_advanced_options = tk.IntVar()

        checkbox_destination_match_source = ttk.Checkbutton(self.root, text="Destination same as Source", variable=var_destination_match_source)
        checkbox_destination_match_source.place(x=450, y=80)

        checkbox_append_hap = ttk.Checkbutton(root, text="Append HAP to filename (preserves version)", variable=var_append_hap)
        checkbox_append_hap.place(x=450, y=120)

        checkbox_create_proxys = ttk.Checkbutton(root, text="Create proxys", variable=var_create_proxys)
        checkbox_create_proxys.place(x=450, y=160)
        checkbox_create_proxys_only = ttk.Checkbutton(root, text="Create proxys only", variable=var_create_proxys_only)
        checkbox_create_proxys_only.place(x=470, y=180)

        checkbox_create_thumbnails = ttk.Checkbutton(root, text="Create thumbnails", variable=var_create_thumbnails)
        checkbox_create_thumbnails.place(x=450, y=220)
        checkbox_create_thumbnails_only = ttk.Checkbutton(root, text="Create thumbnails only", variable=var_create_thumbnails_only)
        checkbox_create_thumbnails_only.place(x=470, y=240)

        checkbox_advanced_options = ttk.Checkbutton(root, text="Advanced Codec Options", variable=var_advanced_options)
        checkbox_advanced_options.place(x=450, y=300)

    def setup_dropdown(self):
        options = ["HAP", "HAP Alpha", "HAP Q", "HAP Q Alpha", "HAP Alpha Only"]
        codec_option = tk.StringVar()  # To store the selected option

        dropdown = ttk.Combobox(self.root, textvariable=self.codec_option, state='readonly')
        dropdown['values'] = options  # Setting the options
        dropdown.current(1)  # Set the default value as the first option
        dropdown.place(x=470, y=325)


    def setup_progressbar(self):
        progressbar_width = 350
        progressbar_height = 40
        canvas_width = progressbar_width
        canvas_height = progressbar_height  # Increase height for status text
        
        progressbar_x = 425
        progressbar_y = 540

        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0)
        self.canvas.place(x=progressbar_x, y=progressbar_y)

        # Use the custom style for the progress bar
        self.progress = ttk.Progressbar(self.canvas, orient=tk.HORIZONTAL, style="text.Horizontal.TProgressbar", length=progressbar_width, mode='determinate')
        self.canvas.create_window(canvas_width/2, canvas_height/2, window=self.progress, width=progressbar_width, height=progressbar_height)


    def update_progress_text(self, text):
        self.style.configure('text.Horizontal.TProgressbar', text=text)


    def console_log_progress(self,percentage):
        self.progress["value"] = percentage
        print(f"Progress: {percentage:.2f}%")

    def drop(self, event):
        """Handles the drop event."""
        widget_name = str(event.widget)
        
        # Handle the source drop area.
        if ".!label" in widget_name:
            self.display_file_tree(event.data)

            if os.path.isdir(event.data):
                self.parent_folder = os.path.basename(os.path.normpath(event.data))
            else:  # It's a file, hence set the folder containing the file as the parent.
                self.parent_folder = os.path.basename(os.path.dirname(event.data))
            
        # Handle the destination drop area.
        elif ".!label2" in widget_name or ".!label3" in widget_name:
            self.display_destination_folder(event.data)
        else:
            print("Unhandled widget:", widget_name)

    def open_file_dialog(self, event):
        """Opens a file dialog based on which label was clicked."""
        file_paths = filedialog.askopenfilenames()
        print(file_paths)
        if file_paths:
            for file_path in file_paths:
                self.display_file_tree(file_path)  # Send each individual file path to be displayed

                if os.path.isdir(file_path):
                    self.parent_folder = os.path.basename(os.path.normpath(file_path))
                else:  # It's a file, hence set the folder containing the file as the parent.
                    self.parent_folder = os.path.basename(os.path.dirname(file_path))



    def open_folder_dialog(self, event):
        """Opens a folder dialog based on which label was clicked."""
        folder_path = filedialog.askdirectory()
        if folder_path:
            # Check which label called this method based on the label's text.
            if "destination" in event.widget.cget("text").lower():
                self.display_destination_folder(folder_path)
            else:
                self.display_file_tree(folder_path)
                self.parent_folder = os.path.basename(os.path.normpath(folder_path))

    def display_file_tree(self, folder_path):
        """Displays the file tree of the specified folder in the Treeview."""

        # Remove the drag prompt if it exists
        if self.tree.exists(self.drag_prompt_id):
            self.tree.delete(self.drag_prompt_id)

        # Check if the path is already in the tree
        for item in self.tree.get_children():
            item_value = self.tree.item(item, 'values')
            if folder_path in item_value:
                print(f"Path {folder_path} already exists in the tree. Skipping...") #this doesnt work with multiple methods
                return

        # If the path is a directory, create a top-level parent node for the directory
        if os.path.isdir(folder_path):
            root_item = self.tree.insert("", "end", text=os.path.basename(folder_path))
            self._populate_tree(root_item, folder_path)
        else:  # If it's a single file
            filename = os.path.basename(folder_path).replace("}", "")
            found_acceptable_extension = any(filename.endswith(container) for container in self.acceptable_containers)

            if found_acceptable_extension:
                self.tree.insert("", "end", text=filename, values=(folder_path,))
            else:
                print(f"FILE EXTENSION ERROR: {filename}")
                return


    def _populate_tree(self, parent, folder_path):
        """Helper method to populate the Treeview with the file structure."""

        # First loop: Handle subdirectories
        for entry in sorted(os.listdir(folder_path)):
            entry_path = os.path.join(folder_path, entry)
            if os.path.isdir(entry_path):  # If it's a sub-directory
                child_item = self.tree.insert(parent, "end", text=entry)  # Create a parent node for sub-directory
                self.tree.item(child_item, open=True)  # Open the tree node by default
                self._populate_tree(child_item, entry_path)  # Recurse into the sub-directory
        
        # Second loop: Handle files
        for entry in sorted(os.listdir(folder_path)):
            entry_path = os.path.join(folder_path, entry)
            if not os.path.isdir(entry_path):  # If it's a file
                filename = os.path.basename(entry_path)
                for container in self.acceptable_containers:
                    if filename.endswith(container):
                        self.tree.insert(parent, "end", text=filename, values=(entry_path,))  # Add as child node to current directory's node

        for item in self.tree.get_children():
            self.tree.item(item, open=True)


    def display_destination_folder(self, folder_path):
        """Displays the selected destination folder."""
        self.destination_label.config(text=folder_path)  # Update the label text with the new destination
        self.destination_path = folder_path   

    def gather_files(self, item_id):
        """Recursively gathers all file paths from a given item (and its children if it's a directory)."""
        item_data = self.tree.item(item_id)
        file_paths = []

        if item_data["values"]:  # It's a file
            file_paths.append(item_data["values"][0])
        else:  # It's a directory
            for child_id in self.tree.get_children(item_id):
                file_paths.extend(self.gather_files(child_id))

        return file_paths
    
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
                all_files_to_encode.extend(self.gather_files(root))
        else:
            for item in selected_items:
                all_files_to_encode.extend(self.gather_files(item))

        # Count the total files to encode
        self.total_files = len(all_files_to_encode)
        print(f"Total number of files to encode: {self.total_files}")

        # Now you can send them to the encoder
        for file_path in all_files_to_encode:
            self.send_to_encoder(file_path)


    def print_all_children(self, parent_item):
        """Recursive function to print all children items under the given parent_item."""
        children = self.tree.get_children(parent_item)
        for child in children:
            child_data = self.tree.item(child)
            if child_data["values"]:
                # It's a file
                self.send_to_encoder(child_data["values"][0])
            else:
                # It's a directory
                # Do NOT call send_to_encoder here, just recurse
                self.print_all_children(child)  # Recurse for the child


    def send_to_encoder(self, file_path):
        # Extract file name and its immediate parent
        file_name = os.path.basename(file_path)
        path_parent = os.path.basename(os.path.dirname(file_path))

        # Decide the destination folder
        if not self.destination_path:
            # Identify the base directory 
            base_path = os.path.dirname(file_path)
            while os.path.basename(base_path) != self.parent_folder and base_path:
                base_path = os.path.dirname(base_path)
            destination_path = os.path.join(base_path, "HAP")
            # destination_path = base_path
        else:
            destination_path = self.destination_path

        # Preserve the subdirectory structure if the immediate parent of the file is not self.parent_folder
        if path_parent != self.parent_folder:
            destination_path = os.path.join(destination_path, path_parent)

        # Construct the final path where the file will be placed/encoded
        final_path = os.path.splitext(os.path.join(destination_path, file_name))[0]
        # print(final_path)
        self.encode_queue.put((file_path, final_path))

        # You can start the encoder thread (if it's not already running):
        if not hasattr(self, "encoder_thread") or not self.encoder_thread.is_alive():
            self.encoder_thread = threading.Thread(target=self.encoder_worker)
            self.encoder_thread.start()

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
        result = encode_to_hap(file_path, final_path, mode="scale", callback=self.console_log_progress)

        if result:
            time.sleep(0.25)
            with self.encode_lock:
                print(f"ELAPSED: {self.elapsed_files}")
                self.elapsed_files += 1

        


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("HAP.py")
    root.geometry("800x600")
    root.configure(bg="#2E2E2E")  # Dark background color
    app = App(root)
    root.mainloop()
