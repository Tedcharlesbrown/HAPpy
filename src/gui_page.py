import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage, font
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD

# ---------------------------------------------------------------------------- #
#                                   SETUP UI                                   #
# ---------------------------------------------------------------------------- #

def setup_ui(self):
    # -------------------------------- BACKGROUND -------------------------------- #
    self.bg = PhotoImage(file = "GUI/assets/background.png") 
    self.background = ttk.Label(self.root, image = self.bg) 
    self.background.place(x = 0, y = 0) 
    # ----------------------------------- INPUT ---------------------------------- #
    # ------------------------- Select A File & Select A Folder ------------------------ #
    self.setup_button(x=25, y=20, width=0, height=0, label_text="Click here to select a file", option="INPUT_FILE", image_path="GUI/assets/Button_SelectAFile.png")
    self.setup_button(x=204, y=20, width=0, height=0, label_text="Click here to select a folder", option="INPUT_FOLDER", image_path="GUI/assets/Button_SelectAFolder.png")
    

    # --------------------------------- Tree View -------------------------------- #
    self.setup_tree_input(x=25, y=80, width=349, height=295, image_path="GUI/assets/Tree_DropArea.png")

    # ---------------------- Clear Selection & Remove Files ---------------------- #

    # -------------------------------- DESTINATION ------------------------------- #
    # --------------------------- Select A Destination --------------------------- #
    self.setup_button(x=430, y=20, width=350, height=40, label_text="Click here to select a destination", option="DESTINATION_FOLDER", image_path="GUI/assets/Button_SelectADestination.png")
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
    self.style = ttk.Style(self.root)
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

def setup_button(self, x, y, width, height, label_text, option, image_path=None):
    
    func = partial(self.open_file_or_folder_dialog, option)

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
    if option == "INPUT_FILE" or option == "INPUT_FOLDER":
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_input_tree(e.data))
    else:
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))

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

    self.canvas = tk.Canvas(self.root, width=width, height=height, bd=0, highlightthickness=0)
    self.canvas.place(x=x, y=y)

    # Use the custom style for the progress bar
    self.progress = ttk.Progressbar(self.canvas, orient=tk.HORIZONTAL, style="text.Horizontal.TProgressbar", length=width, mode='determinate')
    self.canvas.create_window(width/2, height/2, window=self.progress, width=width, height=height)

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

    checkbox_append_hap = ttk.Checkbutton(self.root, text="Append HAP to filename (preserves version)", variable=var_append_hap)
    checkbox_append_hap.place(x=450, y=120)

    checkbox_create_proxys = ttk.Checkbutton(self.root, text="Create proxys", variable=var_create_proxys)
    checkbox_create_proxys.place(x=450, y=160)
    checkbox_create_proxys_only = ttk.Checkbutton(self.root, text="Create proxys only", variable=var_create_proxys_only)
    checkbox_create_proxys_only.place(x=470, y=180)

    checkbox_create_thumbnails = ttk.Checkbutton(self.root, text="Create thumbnails", variable=var_create_thumbnails)
    checkbox_create_thumbnails.place(x=450, y=220)
    checkbox_create_thumbnails_only = ttk.Checkbutton(self.root, text="Create thumbnails only", variable=var_create_thumbnails_only)
    checkbox_create_thumbnails_only.place(x=470, y=240)

    checkbox_advanced_options = ttk.Checkbutton(self.root, text="Advanced Codec Options", variable=var_advanced_options)
    checkbox_advanced_options.place(x=450, y=300)

def setup_dropdown(self):
    options = ["HAP", "HAP Alpha", "HAP Q", "HAP Q Alpha", "HAP Alpha Only"]
    codec_option = tk.StringVar()  # To store the selected option

    dropdown = ttk.Combobox(self.root, textvariable=self.codec_option, state='readonly')
    dropdown['values'] = options  # Setting the options
    dropdown.current(1)  # Set the default value as the first option
    dropdown.place(x=470, y=325)