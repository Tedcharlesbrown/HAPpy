import os
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage, font
from PIL import ImageFont
from tkinter import Entry
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import queue
import time
from functools import partial


from encode import encode_to_hap


class App:
    def __init__(self, root):
        self.root = root
        self.encode_queue = queue.Queue()
        self.encode_lock = threading.Lock()
        self.codec_option = tk.StringVar()
        self.configure_styles()
        self.setup_ui()
        self.acceptable_containers = [".mkv", ".mp4", ".mov", ".asf", ".avi", ".mxf", ".m2p", ".ps", ".ts", ".m2ts", ".mts", ".vob", ".evo", ".3gp", ".3g2", ".f4v", ".flv", ".ogv", ".ogx", ".webm", ".rmvb", ".divx", ".png", ".jpg", ".jpeg", ".tiff", ".svg"]
        self.destination_path = ""
        self.parent_folder = ""
        self.elapsed_files = 1
        self.total_files = 0

    def setup_ui(self):
        # -------------------------------- BACKGROUND -------------------------------- #
        self.bg = PhotoImage(file = "GUI/assets/background.png") 
        self.background = ttk.Label( root, image = self.bg) 
        self.background.place(x = 0, y = 0) 
        # ----------------------------------- INPUT ---------------------------------- #
        # ------------------------- Select A File & Select A Folder ------------------------ #
        open_input_file_dialog = partial(self.open_file_or_folder_dialog, "INPUT_FILE")
        open_input_folder_dialog = partial(self.open_file_or_folder_dialog, "INPUT_FOLDER")
        # self.setup_button(x=25, y=20, width=0, height=0, label_text="Click here to select a file", func=self.open_file_dialog, image_path="GUI/assets/Button_SelectAFile.png")
        # self.setup_button(x=204, y=20, width=0, height=0, label_text="Click here to select a folder", func=self.open_folder_dialog, image_path="GUI/assets/Button_SelectAFolder.png")
        self.setup_button(x=25, y=20, width=0, height=0, label_text="Click here to select a file", func=open_input_file_dialog, image_path="GUI/assets/Button_SelectAFile.png")
        self.setup_button(x=204, y=20, width=0, height=0, label_text="Click here to select a folder", func=open_input_folder_dialog, image_path="GUI/assets/Button_SelectAFolder.png")
        

        # --------------------------------- Tree View -------------------------------- #
        self.setup_tree_input(x=25, y=80, width=349, height=295, image_path="GUI/assets/Tree_DropArea.png")

        # ---------------------- Clear Selection & Remove Files ---------------------- #

        # -------------------------------- DESTINATION ------------------------------- #
        # --------------------------- Select A Destination --------------------------- #
        open_destination_folder_dialog = partial(self.open_file_or_folder_dialog, "DESTINATION_FOLDER")
        # self.setup_button(x=430, y=20, width=350, height=40, label_text="Click here to select a destination", func=self.open_folder_dialog, image_path="GUI/assets/Button_SelectADestination.png")
        self.setup_button(x=430, y=20, width=350, height=40, label_text="Click here to select a destination", func=open_destination_folder_dialog, image_path="GUI/assets/Button_SelectADestination.png")
        # --------------------------------- Tree View -------------------------------- #
        self.setup_output_tree(x=430, y=80, width=350, height=40, image_path="GUI/assets/Tree_Destination.png")

        # ---------------------------------- ENCODE ---------------------------------- #
        encode_selected = partial(self.on_encode_click, True)
        encode_all = partial(self.on_encode_click, False)
        self.setup_encode_buttons(25,540,0,0,"Encode Selected",encode_selected,image_path="GUI/assets/Button_EncodeSelected.png")
        self.setup_encode_buttons(204,540,0,0,"Encode All",encode_all,image_path="GUI/assets/Button_EncodeAll.png")

        # ------------------------------- PROGRESS BAR ------------------------------- #
        self.setup_progressbar(25,480,350,40,image_path="GUI/assets/progressbar.png")

        # -------------------------------- CHECKBOXES -------------------------------- #
        # self.setup_checkboxes()

        # self.setup_dropdown()

    def load_font(self, font_path, size=12):
        # Register the font with tkinter's font factory
        font_name = font.Font(font=font_path, size=size).actual()["family"]
        return font_name

    def configure_styles(self):
        # --------------------------------- VARIABLES -------------------------------- #
        self.style_background = '#1a1a1a'
        self.style_progressbar_background = '#333333'
        self.style_button_background = "#555555"
        self.style_button_foreground = "#FFFFFF"
        self.style_button_pressed = "#444444"
        self.style_button_active = "#5E5E5E"
        # -------------------------------- BACKGROUND -------------------------------- #
        style = ttk.Style()
        self.style = ttk.Style(root)
        style.theme_use("default")
        style.configure("TLabel", background=self.style_background, foreground="#FFFFFF")
        self.font = self.load_font("GUI/assets/LiberationSans-Regular.ttf", size=12)

        # -------------------------------- INPUT TREE -------------------------------- #
        style.configure("Treeview", background="5E5E5E", foreground="#FFFFFF", fieldbackground="#1a1a1a", relief="flat", padding=(0, 3), borderwidth=0)#, font=self.font)
        # -------------------------------- OUTPUT TREE ------------------------------- #
        style.configure("Destination.TLabel", background="#1a1a1a", foreground="#FFFFFF", padding=10, relief="flat", borderwidth=0)#, font=self.font)   
        # ------------------------------ ENCODE BUTTONS ------------------------------ #
        style.configure("TButton", background=self.style_background, foreground=self.style_background, relief="flat", padding=(0), borderwidth=0)
        style.map("TButton", background=[('pressed', self.style_background), ('active', self.style_background)])


        
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
        # style.configure("Dark.TButton", background="#555555", foreground="#FFFFFF", font=("Arial", 14), relief="raised", padding=(20, 10))
        # style.map("Dark.TButton", background=[('pressed', '#333333'), ('active', '#444444')])

        style.layout('text.Horizontal.TProgressbar', 
                         [('Horizontal.Progressbar.trough',
                           {'children': [('Horizontal.Progressbar.pbar',
                                          {'side': 'left', 'sticky': 'ns'})],
                            'sticky': 'nswe'}), 
                          ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
        style.configure('text.Horizontal.TProgressbar', relief='sunken', text='Not Currently Encoding', foreground="white", anchor='center', troughcolor=self.style_background, background='green', borderwidth=0)


    # ---------------------------------------------------------------------------- #
    #                                     INPUT                                    #
    # ---------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------- #
    #                                 INPUT BUTTONS                                #
    # ---------------------------------------------------------------------------- #

    def setup_button(self, x, y, width, height, label_text, func, image_path=None):
        if image_path:
            self.image = tk.PhotoImage(file=image_path)  # Load the image using tk.PhotoImage
            # Retrieve the width and height from the image
            width = self.image.width()
            height = self.image.height()
        else:
            self.image = None

        self.button = ttk.Button(self.root, text=label_text, command=func,style="TButton", image=self.image)
        
        if self.image:
            self.button.image = self.image  # Keep a reference to prevent garbage collection


        self.button.place(x=x, y=y, width=width, height=height)
        self.button.drop_target_register(DND_FILES)
        # self.button.dnd_bind('<<Drop>>', self.source_dropped_on_button)
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_input_tree(e.data))
        # self.button.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
        self.button.bind('<Button-1>', func)

    # ---------------------------------------------------------------------------- #
    #                                  INPUT TREE                                  #
    # ---------------------------------------------------------------------------- #

    def setup_tree_input(self, x, y, width, height, image_path=None):
        if image_path:
            self.image = tk.PhotoImage(file=image_path)  # Load the image using tk.PhotoImage
            # Retrieve the width and height from the image
            width = self.image.width()
            height = self.image.height()
        else:
            self.image = None

        self.tree_input_image = tk.Label(self.root, image=self.image)
        self.tree_input_image.place(x=x, y=y, width=width, height=height)

        if self.image:
            self.tree_iinput_mage = self.image  # Keep a reference to prevent garbage collection

        offset = 6

        self.tree = ttk.Treeview(self.root)
        self.tree.place(x=x + (offset / 2), y=y + (offset / 2), width=width - offset, height=height - offset)
        self.tree['show'] = 'tree'
        self.tree.drop_target_register(DND_FILES)
        # self.tree.dnd_bind('<<Drop>>', self.drop_to_treeview)  # Bind the Drop event
        self.tree.dnd_bind('<<Drop>>', lambda e: self.display_input_tree(e.data))  # Bind the Drop event

        self.drag_prompt_id = self.tree.insert("", "end", text="Drop source file / folder here")

    # ---------------------------------------------------------------------------- #
    #                                 INPUT METHODS                                #
    # ---------------------------------------------------------------------------- #

    # def source_dropped_on_button(self, event): #CALLED IF INPUT IS DROPPED ONTO BUTTONS
    #     self.display_input_tree(event.data)

    # def drop_for_source(self, event):
    #     self.display_input_tree(event.data)

    # def drop_to_treeview(self, event): #CALLED IF INPUT IS DROPPED ONTO FILE TREE
    #     print("DROP TO TREEVIEW")
    #     # widget_type = event.widget.winfo_class()
    #     # if widget_type == "Treeview":
    #     self.display_input_tree(event.data)

    # def open_file_dialog(self, event):
    #     """Opens a file dialog based on which label was clicked."""
    #     file_paths = filedialog.askopenfilenames()
    #     if file_paths:
    #         for file_path in file_paths:
    #             self.display_input_tree(file_path)  # Send each individual file path to be displayed
    #             self.parent_folder = os.path.basename(os.path.dirname(file_path))

    # def open_folder_dialog(self, event):
    #     """Opens a folder dialog based on which label was clicked."""
    #     folder_path = filedialog.askdirectory()
    #     if folder_path:
    #         # Check which label called this method based on the label's text.
    #         if "destination" in event.widget.cget("text").lower():
    #             self.display_destination_folder(folder_path)
    #         else:
    #             self.display_input_tree(folder_path)
    #             self.parent_folder = os.path.basename(os.path.normpath(folder_path))

    # --------------------------- FILE OR FOLDER DIALOG -------------------------- #

    def open_file_or_folder_dialog(self,button,event=None):
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

    # ------------------------------ INPUT FILE TREE ----------------------------- #

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
            print("IS FILE")
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


    # ---------------------------------------------------------------------------- #
    #                                ENCODE BUTTONS                                #
    # ---------------------------------------------------------------------------- #

    def setup_encode_buttons(self, x, y, width, height, label_text, func, image_path=None):
        if image_path:
            self.image = tk.PhotoImage(file=image_path)  # Load the image using tk.PhotoImage
            # Retrieve the width and height from the image
            width = self.image.width()
            height = self.image.height()
        else:
            self.image = None
        
        self.button_encode = ttk.Button(self.root, text=label_text, style="TButton", command=func, image=self.image)
 
        if self.image:
            self.button_encode.image = self.image  # Keep a reference to prevent garbage collection

        self.button_encode.place(x=x, y=y)

    # ---------------------------------------------------------------------------- #
    #                                  OUTPUT TREE                                 #
    # ---------------------------------------------------------------------------- #

    def setup_output_tree(self, x, y, width, height, image_path=None):
        if image_path:
            self.image = tk.PhotoImage(file=image_path)  # Load the image using tk.PhotoImage
            # Retrieve the width and height from the image
            width = self.image.width()
            height = self.image.height()
        else:
            self.image = None


        self.tree_output_image = tk.Label(self.root, image=self.image)
        self.tree_output_image.place(x=x, y=y, width=width, height=height)

        if self.image:
            self.tree_output_image = self.image  # Keep a reference to prevent garbage collection

        offset = 6

        self.destination_label = ttk.Label(self.root, text="Drop destination folder here", wraplength=300, style="Destination.TLabel")
        self.destination_label.place(x=x + (offset / 2), y=y + (offset / 2), width=width - offset, height=height - offset)
        self.destination_label.drop_target_register(DND_FILES)
        self.destination_label.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
        # self.destination_label.bind('<Button-1>', self.open_folder_dialog)


    def display_destination_folder(self, folder_path):
        """Displays the selected destination folder."""
        self.destination_label.config(text=folder_path)  # Update the label text with the new destination
        self.destination_path = folder_path  

    # ---------------------------------------------------------------------------- #
    #                                 PROGRESS BAR                                 #
    # ---------------------------------------------------------------------------- #

    def setup_progressbar(self,x,y,width,height,image_path=None):
        if image_path:
            self.image = tk.PhotoImage(file=image_path)  # Load the image using tk.PhotoImage
            # Retrieve the width and height from the image
            width = self.image.width()
            height = self.image.height()
        else:
            self.image = None
    
        self.progressbar_image = tk.Label(self.root, image=self.image)
        self.progressbar_image.place(x=x, y=y, width=width, height=height)

        if self.image:
            self.progressbar_image = self.image  # Keep a reference to prevent garbage collection

        offset = 6

        x = x + offset / 2
        y = y + offset / 2
        width = width - offset
        height = height - offset
    
        self.canvas = tk.Canvas(root, width=width, height=height, bd=0, highlightthickness=0)
        self.canvas.place(x=x, y=y)

        # Use the custom style for the progress bar
        self.progress = ttk.Progressbar(self.canvas, orient=tk.HORIZONTAL, style="text.Horizontal.TProgressbar", length=width, mode='determinate')
        self.canvas.create_window(width/2, height/2, window=self.progress, width=width, height=height)

    def update_progress_text(self, text):
        self.style.configure('text.Horizontal.TProgressbar', text=text)


    def console_log_progress(self,percentage):
        self.progress["value"] = percentage
        print(f"Progress: {percentage:.2f}%")

    # ---------------------------------------------------------------------------- #
    #                                  CHECKBOXES                                  #
    # ---------------------------------------------------------------------------- #

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

        # Now you can send them to the encoder
        for file_path in all_files_to_encode:
            print(file_path, self.destination_path)
            self.send_to_encoder(file_path)

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

    # def print_all_children(self, parent_item):
    #     """Recursive function to print all children items under the given parent_item."""
    #     children = self.tree.get_children(parent_item)
    #     for child in children:
    #         child_data = self.tree.item(child)
    #         if child_data["values"]:
    #             # It's a file
    #             self.send_to_encoder(child_data["values"][0])
    #         else:
    #             # It's a directory
    #             # Do NOT call send_to_encoder here, just recurse
    #             self.print_all_children(child)  # Recurse for the child


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
            # self.encoder_thread.start()

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


# ---------------------------------------------------------------------------- #
#                                     MAIN                                     #
# ---------------------------------------------------------------------------- #

# def on_drag(event):
#     x, y = event.x_root, event.y_root
#     root.geometry(f'+{x - offset[0]}+{y - offset[1]}')

# def on_click(event):
#     global offset
#     offset = (event.x, event.y)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("HAP.py")
    root.geometry("800x600")
    root.configure(bg="#2E2E2E")  # Dark background color
    # root.overrideredirect(True)  # remove title bar

    # # Create a custom title bar
    # title_bar = tk.Frame(root, bg="black", height=30)
    # title_bar.pack(fill=tk.X, side=tk.TOP)

    # # Close button
    # close_button = ttk.Button(title_bar, text="X", command=root.quit)
    # close_button.pack(side=tk.RIGHT)

    # # Enable dragging of the window
    # title_bar.bind("<Button-1>", on_click)
    # title_bar.bind("<B1-Motion>", on_drag)


    # # Sample ttk.Button for demonstration
    # sample_button = ttk.Button(root, text="Sample Button")
    # sample_button.pack(pady=20)

    app = App(root)

    # title_bar.lift()  # this will bring title_bar to the top
    
    root.mainloop()
