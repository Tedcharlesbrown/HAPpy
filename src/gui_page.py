import tkinter as tk
from tkinter import ttk,PhotoImage, font
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD

from autopytoexe_path import resource_path

# ---------------------------------------------------------------------------- #
#                                   SETUP UI                                   #
# ---------------------------------------------------------------------------- #



def setup_ui(self):
    # -------------------------------- BACKGROUND -------------------------------- #
    self.bg = PhotoImage(file=resource_path("GUI/assets/background.png")) 
    self.background = ttk.Label(self.root, image = self.bg) 
    self.background.place(x = 0, y = 0) 
    # ----------------------------------- INPUT ---------------------------------- #
    # ------------------------- Select A File & Select A Folder ------------------------ #
    self.setup_button(x=25, y=20, width=0, height=0, label_text="Click here to select a file", option="INPUT_FILE", image_path="GUI/assets/Button_SelectAFile.png")
    self.setup_button(x=204, y=20, width=0, height=0, label_text="Click here to select a folder", option="INPUT_FOLDER", image_path="GUI/assets/Button_SelectAFolder.png")
    # --------------------------------- Tree View -------------------------------- #
    self.setup_tree_input(x=25, y=80, width=349, height=295, image_path="GUI/assets/Tree_DropArea.png")
    # ---------------------- Clear Selection & Remove Files ---------------------- #
    self.setup_button(x=25, y=400, width=0, height=0, label_text="Clear Selection", option="CLEAR_SELECTION", image_path="GUI/assets/Button_ClearSelection.png")
    self.setup_button(x=204, y=400, width=0, height=0, label_text="Remove Files", option="REMOVE_FILES", image_path="GUI/assets/Button_RemoveFiles.png")
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
    self.var_destination_same_as_source = tk.IntVar(value=1)
    self.setup_checkboxes(430,160,"Destination same as Source", self.var_destination_same_as_source)
    self.var_create_hap_folder_at_source = tk.IntVar(value=1)
    self.setup_checkboxes(455,187,"Create HAP folder at Source (preserves subfolders)", self.var_create_hap_folder_at_source)
    self.var_append_hap_to_file_name = tk.IntVar()
    self.setup_checkboxes(430,228,"Append HAP to filename (preserves version tag)", self.var_append_hap_to_file_name)
    self.var_advanced_options = tk.IntVar()
    self.setup_checkboxes(430,263,"Advanced options", self.var_advanced_options)

    # self.setup_dropdown()

def load_font(self, font_path, size=12):
        # Register the font with tkinter's font factory
        font_name = font.Font(font=font_path, size=size).actual()["family"]
        return font_name

def configure_styles(self):
    # --------------------------------- VARIABLES -------------------------------- #
    self.style_background = '#1d1d1d'
    self.style_progressbar_background = '#333333'
    self.style_button_background = "#555555"
    self.style_button_foreground = "#FFFFFF"
    self.style_button_pressed = "#444444"
    self.style_button_active = "#5E5E5E"
    # ---------------------------------- IMAGES ---------------------------------- #
    self.checkbox_on_image = PhotoImage(file=resource_path("GUI/assets/Checkbox_on.png"))
    self.checkbox_off_image = PhotoImage(file=resource_path("GUI/assets/Checkbox_off.png"))
    self.radio_on_image = PhotoImage(file=resource_path("GUI/assets/Radio_on.png"))
    self.radio_off_image = PhotoImage(file=resource_path("GUI/assets/Radio_off.png"))
    # -------------------------------- BACKGROUND -------------------------------- #
    style = ttk.Style()
    self.style = ttk.Style(self.root)
    style.theme_use("default")
    style.layout('Custom.TCheckbutton', [('Checkbutton.label', {'sticky': 'nswe'})])
    style.configure("TLabel", background=self.style_background, foreground="#FFFFFF")
    self.font = self.load_font("GUI/assets/LiberationSans-Regular.ttf", size=12)

    # -------------------------------- INPUT TREE -------------------------------- #
    style.configure("Treeview", background="5E5E5E", foreground="#FFFFFF", fieldbackground="#1a1a1a", relief="flat", padding=(0, 3), borderwidth=0)#, font=self.font)
    # -------------------------------- OUTPUT TREE ------------------------------- #
    style.configure("Destination.TLabel", background="#1a1a1a", foreground="#FFFFFF", padding=10, relief="flat", borderwidth=0)#, font=self.font)   
    # ------------------------------ ENCODE BUTTONS ------------------------------ #
    style.configure("TButton", background=self.style_background, foreground=self.style_background, relief="flat", padding=(0), borderwidth=0)
    style.map("TButton", background=[('pressed', self.style_background), ('active', self.style_background)])

    # -------------------------------- CHECKBOXES -------------------------------- #
    style.configure('Custom.TCheckbutton',
                    indicatoron=False,
                    background=self.style_background,
                    relief='flat',
                    image=self.checkbox_off_image)
    style.map('Custom.TCheckbutton',
            image=[('selected', self.checkbox_on_image)])
    style.configure("Checkbox.TLabel", background=self.style_background, foreground="#FFFFFF")
    
    
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

    style.layout('text.Horizontal.TProgressbar', 
                        [('Horizontal.Progressbar.trough',
                        {'children': [('Horizontal.Progressbar.pbar',
                                        {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}), 
                        ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
    style.configure('text.Horizontal.TProgressbar', relief='sunken', text='Not Currently Encoding', foreground="white", anchor='center', troughcolor=self.style_background, background='green', borderwidth=0)
    
    style.configure("Dialog.TLabel", background=self.style_background, foreground="#FFFFFF")
    style.configure("Dialog.TButton", background="black", foreground="white", relief="flat", padding=(0), borderwidth=0)
    style.map("Dialog.TButton", background=[('pressed', self.style_background), ('active', self.style_background)])

# ---------------------------------------------------------------------------- #
#                                     INPUT                                    #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
#                                 INPUT BUTTONS                                #
# ---------------------------------------------------------------------------- #

def setup_button(self, x, y, width, height, label_text, option, image_path=None):
    
    func = partial(self.open_file_or_folder_dialog, option)

    if image_path:
        self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
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
    elif option == "DESTINATION_FOLDER":
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
    elif option == "CLEAR_SELECTION":
        self.button["command"] = self.remove_selection
    elif option == "REMOVE_FILES":
        self.button["command"] = self.clear_file_tree

    # self.button.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
    self.button.bind('<Button-1>', func)

# ---------------------------------------------------------------------------- #
#                                  INPUT TREE                                  #
# ---------------------------------------------------------------------------- #

def setup_tree_input(self, x, y, width, height, image_path=None):
    if image_path:
        self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
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
            self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
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
        self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
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
        self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
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

def setup_checkboxes(self, x, y, text, variable):
    checkbox = ttk.Checkbutton(self.root, text=text, variable=variable, style='Custom.TCheckbutton')
    checkbox.place(x=x, y=y)

    label = ttk.Label(self.root, text=text, style="Checkbox.TLabel")
    label.place(x=x + 25, y=y-1)  

def setup_dropdown(self):
    options = ["HAP", "HAP Alpha", "HAP Q", "HAP Q Alpha", "HAP Alpha Only"]
    codec_option = tk.StringVar()  # To store the selected option

    dropdown = ttk.Combobox(self.root, textvariable=self.codec_option, state='readonly')
    dropdown['values'] = options  # Setting the options
    dropdown.current(1)  # Set the default value as the first option
    dropdown.place(x=470, y=325)


def update_progress_text(self, text):
    self.style.configure('text.Horizontal.TProgressbar', text=text)

def console_log_progress(self, percentage):
    self.progress["value"] = percentage
    print(f"Progress: {percentage:.2f}%")


# ---------------------------------------------------------------------------- #
#                            OVERWRITE CONFIRMATION                            #
# ---------------------------------------------------------------------------- #
def trigger_overwrite_popup(self):
    dialog = tk.Toplevel(self.root)
    dialog.title("Overwrite Confirmation")

    # Set the size of the dialog
    dialog.geometry("350x180")  # Width x Height
    # Set the dialog's background color
    dialog.configure(bg="#1a1a1a")

    # Load the background image
    self.popup_bg_image = tk.PhotoImage(file=resource_path("GUI/assets/Popup_Background.png"))
    popup_bg_label = tk.Label(dialog, image=self.popup_bg_image, bd=0)
    popup_bg_label.place(x=0, y=0)
    # dialog.geometry(f"{self.bg_image.width()}x{self.bg_image.height()}")

    # Make the dialog non-resizable
    dialog.resizable(False, False)
    
    # Use the custom style for the label inside the dialog
    msg = ttk.Label(dialog, text="The file already exists. Do you want to overwrite it?", style="Dialog.TLabel")
    msg.pack(pady=10, padx=10)
    
    def on_yes_all():
        dialog.result = ("YES TO ALL")
        dialog.destroy()

    def on_yes():
        dialog.result = ("YES")
        dialog.destroy()

    def on_skip():
        dialog.result = ("SKIP")
        dialog.destroy()


    self.yes_all_image = tk.PhotoImage(file=resource_path("GUI/assets/Popup_YesAll.png"))
    yes_all_btn = ttk.Button(dialog, text="Yes to all", command=on_yes_all, style="Dialog.TButton", image=self.yes_all_image)
    yes_all_btn.place(x=10, y=130, width=self.yes_all_image.width(), height=self.yes_all_image.height())

    self.yes_image = tk.PhotoImage(file=resource_path("GUI/assets/Popup_Yes.png"))
    yes_btn = ttk.Button(dialog, text="Yes", command=on_yes, style="Dialog.TButton", image=self.yes_image)
    yes_btn.place(x=125, y=130, width=self.yes_image.width(), height=self.yes_image.height())

    self.skip_image = tk.PhotoImage(file=resource_path("GUI/assets/Popup_Skip.png"))
    skip_btn = ttk.Button(dialog, text="Skip", command=on_skip, style="Dialog.TButton", image=self.skip_image)
    skip_btn.place(x=240, y=130, width=self.skip_image.width(), height=self.skip_image.height())

    # Force the dialog to update its layout and dimensions
    dialog.update_idletasks()

    # Center the dialog relative to its parent
    parent_x = self.root.winfo_x()
    parent_y = self.root.winfo_y()
    parent_width = self.root.winfo_width()
    parent_height = self.root.winfo_height()

    dialog_width = dialog.winfo_width()
    dialog_height = dialog.winfo_height()

    dialog_x = parent_x + (parent_width // 2) - (dialog_width // 2)
    dialog_y = parent_y + (parent_height // 2) - (dialog_height // 2)

    dialog.geometry(f"+{dialog_x}+{dialog_y}")

    dialog.lift()
    dialog.grab_set()
    dialog.wait_window()

    return dialog.result

