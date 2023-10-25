import tkinter as tk
from tkinter import ttk,PhotoImage, font
from functools import partial
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

from autopytoexe_path import resource_path

# ---------------------------------------------------------------------------- #
#                                   SETUP UI                                   #
# ---------------------------------------------------------------------------- #

def setup_constants(self):
    self.acceptable_containers = [".mkv", ".mp4", ".mov", ".asf", ".avi", ".mxf", ".m2p", ".ps", ".ts", ".m2ts", ".mts", ".vob", ".evo", ".3gp", ".3g2", ".f4v", ".flv", ".ogv", ".ogx", ".webm", ".rmvb", ".divx", ".png", ".jpg", ".jpeg", ".tiff", ".svg"]

    self.style_background = '#1d1d1d'
    self.style_progressbar_background = '#333333'
    self.style_tree_background = '#2d2d2d'
    self.style_button_background = "#2d2d2d"
    self.style_button_foreground = "#FFFFFF"
    self.style_button_pressed = "#444444"
    self.style_button_active = "#5E5E5E"

def setup_ui(self):
    # -------------------------------- BACKGROUND -------------------------------- #
    self.bg = PhotoImage(file=resource_path("background.png")) 
    self.background = ttk.Label(self.root, image = self.bg, border=0) 
    self.background.place(x = 0, y = 0)
    # ----------------------------------- INPUT ---------------------------------- #
    # ------------------------- Select A File & Select A Folder ------------------------ #
    self.setup_button(x=25, y=20, text="Select a file", option="INPUT_FILE", image_path="Button_Medium.png")
    self.setup_button(x=204, y=20, text="Select a folder", option="INPUT_FOLDER", image_path="Button_Medium.png")
    # --------------------------------- Tree View -------------------------------- #
    self.setup_tree(x=25, y=80, tree_type="INPUT", image_path="Tree_Input.png")
    # ---------------------- Clear Selection & Remove Files ---------------------- #
    self.setup_button(x=25, y=400, text="Clear selection", option="CLEAR_SELECTION", image_path="Button_Medium.png")
    self.setup_button(x=204, y=400, text="Remove files", option="REMOVE_FILES", image_path="Button_Medium.png")
    # -------------------------------- DESTINATION ------------------------------- #
    # --------------------------- Select A Destination --------------------------- #
    self.setup_button(x=430, y=20, text="Select a destination", option="DESTINATION_FOLDER", image_path="Button_Large.png")
    # --------------------------------- Tree View -------------------------------- #
    self.setup_tree(x=430, y=80, tree_type="OUTPUT", image_path="Tree_Destination.png")

    # ---------------------------------- ENCODE ---------------------------------- #
    self.setup_button(x=25, y=540, text="Encode Selected   ",option="ENCODE_SELECTED", image_path="Button_EncodeSelected.png")
    self.setup_button(x=204, y=540, text="Encode All",option="ENCODE_ALL", image_path="Button_EncodeAll.png")


    # ------------------------------- PROGRESS BAR ------------------------------- #
    self.setup_progressbar(25,480,350,40,image_path="progressbar.png")


    # ---------------------------- CHECKBOX VARIABLES ---------------------------- #
    self.var_destination_same_as_source = tk.IntVar(value=1)
    self.var_create_hap_folder_at_source = tk.IntVar(value=0)
    self.var_append_hap_to_file_name = tk.IntVar(value=1)
    self.var_advanced_options = tk.IntVar(value=0)
    self.var_create_proxys = tk.IntVar(value=0)
    self.var_only_create_proxys = tk.IntVar(value=0),
    self.var_codec_option = tk.StringVar(value="hap_alpha")
    self.var_scale_option = tk.StringVar(value="stretch")


    # -------------------------------- CHECKBOXES -------------------------------- #
    self.setup_checkboxes(430,171,"Destination same as Source", self.var_destination_same_as_source)
    self.setup_checkboxes(450,206,"Create HAP folder at Source", self.var_create_hap_folder_at_source)
    self.setup_checkboxes(430,241,"Append HAP to filename (preserves version tag)", self.var_append_hap_to_file_name)
    self.setup_checkboxes(430,276,"Advanced options", self.var_advanced_options)

    # ---------------------------------------------------------------------------- #
    #                               ADVANCED OPTIONS                               #
    # ---------------------------------------------------------------------------- #

    self.advanced_options_image = tk.PhotoImage(file=resource_path("AdvancedMenu.png"))
    self.advanced_options_bg = ttk.Label(self.root, image=self.advanced_options_image, borderwidth=0, style="TLabel")
    self.advanced_options_bg.place(x=430, y=310, width=self.advanced_options_image.width(), height=self.advanced_options_image.height())
    self.advanced_options_bg.image = self.advanced_options_image  # Keep a reference to the image to prevent garbage collection
    self.advanced_options_bg.lower()

    # ----------------------------------- RADIO ---------------------------------- #
    self.setup_radio(454,351 ,"HAP", self.var_codec_option, "hap", True)
    self.setup_radio(512,351 ,"HAP Alpha", self.var_codec_option, "hap_alpha", True)
    self.setup_radio(570,351 ,"HAP Q", self.var_codec_option, "hap_q", True)

    self.setup_radio(657,351,"Stretch", self.var_scale_option, "stretch", True)
    # self.setup_radio(686,351,"Scale", self.var_scale_option, "scale", True)
    self.setup_radio(715,351,"Pad", self.var_scale_option, "pad", True)

    # ----------------------------------- PROXY ---------------------------------- #
    self.setup_checkboxes(450,431,"Create Proxys", self.var_create_proxys, True)
    self.setup_checkboxes(470,461,"Only create Proxys", self.var_only_create_proxys, True)
    

def load_font(self, font_path, size=12):
        # Register the font with tkinter's font factory
        font_name = font.Font(font=font_path, size=size).actual()["family"]
        return font_name

def configure_styles(self):
    # ---------------------------------- IMAGES ---------------------------------- #
    self.advanced_options_image = PhotoImage(file=resource_path("AdvancedMenu.png"))
    self.checkbox_on_image = PhotoImage(file=resource_path("Checkbox_on.png"))
    self.checkbox_off_image = PhotoImage(file=resource_path("Checkbox_off.png"))
    self.radio_on_image = PhotoImage(file=resource_path("radio_on.png"))
    self.radio_off_image = PhotoImage(file=resource_path("radio_off.png"))
    # -------------------------------- BACKGROUND -------------------------------- #
    style = ttk.Style()
    self.style = ttk.Style()
    style.theme_use("default")
    style.layout('Custom.TCheckbutton', [('Checkbutton.label', {'sticky': 'nswe'})])
    style.configure("TLabel", background=self.style_background, foreground="#FFFFFF")
    self.font = self.load_font("LiberationSans-Regular.ttf")
    self.font_bold = self.load_font("LiberationSans-Bold.ttf")
    # ----------------------------------- ICON ----------------------------------- #
    icon_photo = tk.PhotoImage(file=resource_path('icon.png'))
    self.root.wm_iconphoto(False, icon_photo)

    # ---------------------------------------------------------------------------- #
    #                                    BUTTONS                                   #
    # ---------------------------------------------------------------------------- #
    style.configure("TButton", background=self.style_background, foreground=self.style_button_foreground, relief="raised", padding=(-1,-1), borderwidth=0, font=(self.font, 10))
    style.map("TButton", background=[('pressed', self.style_background), ('active', self.style_background)])


    # -------------------------------- INPUT TREE -------------------------------- #
    style.configure("Treeview", background=self.style_tree_background, foreground="#FFFFFF", fieldbackground=self.style_tree_background, relief="flat", padding=(0, 5), borderwidth=0, font=(self.font, 10))
    # -------------------------------- OUTPUT TREE ------------------------------- #
    style.configure("Destination.TLabel", background=self.style_tree_background, foreground="#FFFFFF", padding=(10,5), relief="flat", borderwidth=0, font=(self.font, 10))

    # -------------------------------- CHECKBOXES -------------------------------- #
    style.configure('Custom.TCheckbutton',
                    indicatoron=False,
                    background=self.style_background,
                    relief='flat',
                    image=self.checkbox_off_image)
    style.map('Custom.TCheckbutton',
            image=[('selected', self.checkbox_on_image)])
    style.configure("Checkbox.TLabel", background=self.style_background, foreground="#FFFFFF", font=(self.font, 10))
    
    
    style.configure("TCheckbutton", background="#2E2E2E", foreground="#FFFFFF", relief="flat")
    style.map("TCheckbutton", background=[('active', '#2E2E2E')], indicatorcolor=[("selected", "#555555")], indicatorrelief=[('pressed', 'sunken'), ('!pressed', 'raised')])
    style.configure("TCheckbutton", font=100)

    # -------------------------- Advanced Options Button ------------------------- #
    # style.configure("Advanced.TLabel", background=self.style_background, foreground="#FFFFFF")
    


    # ------------------------------- RADIO BUTTONS ------------------------------ #
    self.style.layout("TRadiobutton", [
        ("Radiobutton.padding", {
            "children": [
                ("CustomRadioIndicator", {"side": "left", "sticky": "ns"}),
                ("Radiobutton.label", {"side": "left", "sticky": ""})
            ]
        })
    ])
    self.style.element_create("CustomRadioIndicator", "image", self.radio_off_image, ("selected", self.radio_on_image), border=0, sticky="ew")    
    self.style.configure("TRadiobutton",
                background=self.style_background,
                foreground="white",  # Text color
                font=("Arial", 10),
                anchor="center",
                indicator="CustomRadioIndicator",  # Use the custom element
                # width=self.radio_off_image.width(),  # Set the width to match the image's width
                compound="left")  # Ensure the image is to the left of the text
    self.style.map("TRadiobutton",
               foreground=[('active', self.style_background)],
               background=[('active', self.style_background)]
               )
    
    self.style.configure("Radio.TLabel", anchor="center")

    # ------------------------------- PROGRESS BAR ------------------------------- #
    style.layout('text.Horizontal.TProgressbar', 
                        [('Horizontal.Progressbar.trough',
                        {'children': [('Horizontal.Progressbar.pbar',
                                        {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}), 
                        ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
    style.configure('text.Horizontal.TProgressbar', relief='sunken', text='Not Currently Encoding', foreground="white", anchor='center', troughcolor=self.style_background, background='green', borderwidth=0, font=(self.font, 9))
    
    # ---------------------------------------------------------------------------- #
    #                                     POPUP                                    #
    # ---------------------------------------------------------------------------- #
    style.configure("popup.TLabel", background=self.style_background, foreground="#FFFFFF", font=(self.font, 11), anchor="center")
    style.configure("popup.TButton", background="black", foreground="white", relief="flat", padding=(0), borderwidth=0)
    style.map("popup.TButton", background=[('pressed', self.style_background), ('active', self.style_background)])

# ---------------------------------------------------------------------------- #
#                                     INPUT                                    #
# ---------------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #
#                                 INPUT BUTTONS                                #
# ---------------------------------------------------------------------------- #
def setup_button(self, x, y, text, option, image_path=None):
    func = None
    self.image = tk.PhotoImage(file=resource_path(image_path))  # Load the image using tk.PhotoImage
    width = self.image.width()
    height = self.image.height()


    self.button = ttk.Button(self.root, text=text, command=func,style="TButton", image=self.image, compound='center')
    
    if self.image:
        self.button.image = self.image  # Keep a reference to prevent garbage collection

    self.button.place(x=x, y=y, width=width, height=height)
    self.button.drop_target_register(DND_FILES)
    self.button['takefocus'] = False
    if option == "INPUT_FILE" or option == "INPUT_FOLDER":
        self.button["command"] = partial(self.open_file_or_folder_dialog, option)
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_input_tree(e.data))
    elif option == "DESTINATION_FOLDER":
        self.button["command"] = partial(self.open_file_or_folder_dialog, option)
        self.button.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
    elif option == "CLEAR_SELECTION":
        self.button["command"] = self.clear_selection
    elif option == "REMOVE_FILES":
        self.button["command"] = self.remove_file_from_tree
    elif option == "ENCODE_SELECTED":
        self.button["command"] = partial(self.on_encode_click, True)
    elif option == "ENCODE_ALL":
        self.button["command"] = partial(self.on_encode_click, False)
    else:
        raise ValueError("Invalid argument. Please use 'INPUT_FILE', 'INPUT_FOLDER', 'DESTINATION_FOLDER', 'CLEAR_SELECTION', 'REMOVE_FILES', 'ENCODE_SELECTED', or 'ENCODE_ALL'.")

# ---------------------------------------------------------------------------- #
#                                  INPUT TREE                                  #
# ---------------------------------------------------------------------------- #

def setup_tree(self, x, y, tree_type="INPUT", image_path=None):
    
    image = tk.PhotoImage(file=resource_path(image_path))
    img_width = image.width()
    img_height = image.height()

    tree_image = tk.Label(self.root, image=image)
    tree_image.place(x=x, y=y, width=img_width, height=img_height)
    tree_image.image = image  # Keep a reference to the image to prevent garbage collection


    offset = 6
    adjusted_x = x + (offset / 2)
    adjusted_y = y + (offset / 2)
    adjusted_width = img_width - offset
    adjusted_height = img_height - offset

    if tree_type == "INPUT":
        self.tree = ttk.Treeview(self.root)
        self.tree.place(x=adjusted_x, y=adjusted_y, width=adjusted_width, height=adjusted_height)
        self.tree['show'] = 'tree'
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', lambda e: self.handle_input_drop(e.data))
        self.drag_prompt_id = self.tree.insert("", "end", text="Drop source file / folder here")
    elif tree_type == "OUTPUT":
        self.destination_label = ttk.Label(self.root, text="Drop destination folder here", wraplength=300, style="Destination.TLabel", anchor="nw")
        self.destination_label.place(x=adjusted_x, y=adjusted_y, width=adjusted_width, height=adjusted_height)
        self.destination_label.drop_target_register(DND_FILES)
        self.destination_label.dnd_bind('<<Drop>>', lambda e: self.display_destination_folder(e.data))
    else:
        raise ValueError("tree_type must be 'INPUT' or 'OUTPUT'")

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

def setup_checkboxes(self, x, y, text, variable, hidden=None):
    checkbox = ttk.Checkbutton(self.root, text=text, variable=variable, style='Custom.TCheckbutton', command=lambda: self.handle_checkbox_toggle())
    checkbox.place(x=x, y=y)

    label = ttk.Label(self.root, text=text, style="Checkbox.TLabel")
    label_x_offset = x + 25
    label_y_offset = y - 1
    label.place(x=label_x_offset, y=label_y_offset)  

    # Store checkbox and label in a dictionary
    self.advanced_options_widgets[text] = (checkbox, label)

    if hidden:
        checkbox.lower()
        label.lower()

def handle_checkbox_toggle(self):
    def hide_advanced_options(key):
        self.advanced_options_bg.lower()
        radio, label = self.advanced_options_widgets[key]
        radio.lower()
        label.lower()

    def show_advanced_options(key):
        radio, label = self.advanced_options_widgets[key]
        radio.lift()
        label.lift()

    if not self.var_destination_same_as_source.get():
        self.var_create_hap_folder_at_source.set(False)

    if self.var_advanced_options.get():
        self.advanced_options_bg.lift()
        for option_key in ["hap", "hap_alpha", "hap_q", "stretch", "pad", "Create Proxys", "Only create Proxys"]:
            show_advanced_options(option_key)
    else:
        for option_key in ["hap", "hap_alpha", "hap_q", "stretch", "pad", "Create Proxys", "Only create Proxys"]:
            hide_advanced_options(option_key)

def setup_radio(self, x, y, text, variable, value, hidden=None):
    radio = ttk.Radiobutton(self.root, text=None, variable=variable, value=value, style='TRadiobutton')
    radio.place(x=x, y=y)

    label = ttk.Label(self.root, text=text, style="Radio.TLabel")
    label_x_offset = x + 9
    label_y_offset = y + 30
    label.place(x=label_x_offset, y=label_y_offset, anchor="center")

    # Store radio and label in a dictionary
    self.advanced_options_widgets[value] = (radio, label)

    if hidden:
        radio.lower()
        label.lower()


def update_progress_text(self, text):
    self.style.configure('text.Horizontal.TProgressbar', text=text)

def console_log_progress(self, percentage):
        self.progress["value"] = percentage
        percentage = int(percentage)

        if self.progress_bar_update:
            if percentage < self.progress_bar_next_update:
                return
            else:
                # self.console.log(f"Encoding progress: {percentage}%", "ENCODE")
                self.console.log(f"Encoding progress: {self.progress_bar_next_update}%", "ENCODE")
                if percentage < 25:
                    self.progress_bar_next_update = 25
                elif percentage < 50:
                    self.progress_bar_next_update = 50
                elif percentage < 75:
                    self.progress_bar_next_update = 75
                elif percentage < 100:
                    self.progress_bar_next_update = 100
                else:
                    self.progress_bar_next_update = 101 
                self.progress_bar_update = False
        elif percentage >= self.progress_bar_next_update:
            self.progress_bar_update = True



# ---------------------------------------------------------------------------- #
#                            OVERWRITE CONFIRMATION                            #
# ---------------------------------------------------------------------------- #
def trigger_overwrite_popup(self, message):
    popup = tk.Toplevel(self.root)
    popup.title("Overwrite Confirmation")
    popup.geometry("400x200") 
    # popup.configure(bg="#1a1a1a")

    self.popup_bg_image = tk.PhotoImage(file=resource_path("Popup_Background.png"))
    popup_bg_label = tk.Label(popup, image=self.popup_bg_image, bd=0)
    popup_bg_label.place(x=0, y=0)
    popup.resizable(False, False)
    
    header_text = "The file already exists. Do you want to overwrite it?"
    
    message_prefix = os.path.dirname(message)
    message_suffix = os.path.basename(message)
    # Use the custom style for the label inside the popup
    popup_header = ttk.Label(popup, text=header_text, style="popup.TLabel", anchor='center', justify='center', font=(self.font, 11))
    popup_header.pack(pady=10, padx=10)
    popup_message = ttk.Label(popup, text=message_prefix +"\n" + message_suffix, style="popup.TLabel", anchor='center', font=(self.font, 10))
    popup_message.pack(pady=10, padx=10)

    def on_yes():
        popup.result = ("YES")
        popup.destroy()

    def on_skip():
        popup.result = ("SKIP")
        popup.destroy()

    self.popup_button_image = tk.PhotoImage(file=resource_path("Button_Small.png"))
    width = self.popup_button_image.width()
    height = self.popup_button_image.height()

    # --------------------------------- CHECKBOX --------------------------------- #
    popup_variable = tk.IntVar(value=0)
    # checkbox = ttk.Checkbutton(popup, text="TEST", variable=popup_variable, style='Custom.TCheckbutton', command=lambda: self.handle_checkbox_toggle())
    # checkbox.place(x=27, y=161)

    # label = ttk.Label(popup, text="Do not ask again", style="Checkbox.TLabel")
    # label.place(x=55, y=159)  

    # ------------------------------------ YES ----------------------------------- #

    yes_btn = ttk.Button(popup, text="Yes", command=on_yes, style="TButton", image=self.popup_button_image, compound='center')
    yes_btn.place(x=178, y=150, width=width, height=height)
    yes_btn['takefocus'] = False

    # ------------------------------------ NO ------------------------------------ #

    skip_btn = ttk.Button(popup, text="No", command=on_skip, style="TButton", image=self.popup_button_image, compound='center')
    skip_btn.place(x=291, y=150, width=width, height=height)
    skip_btn['takefocus'] = False

    # Force the popup to update its layout and dimensions
    popup.update_idletasks()

    # Center the popup relative to its parent
    parent_x = self.root.winfo_x()
    parent_y = self.root.winfo_y()
    parent_width = self.root.winfo_width()
    parent_height = self.root.winfo_height()

    popup_width = popup.winfo_width()
    popup_height = popup.winfo_height()

    popup_x = parent_x + (parent_width // 2) - (popup_width // 2)
    popup_y = parent_y + (parent_height // 2) - (popup_height // 2)

    popup.geometry(f"+{popup_x}+{popup_y}")

    popup.lift()
    popup.grab_set()
    popup.wait_window()

    return popup.result, popup_variable.get()






# ---------------------------------------------------------------------------- #
#                                    PLAYER                                    #
# ---------------------------------------------------------------------------- #

def setup_player(self):
    def drop(event):
        file_path = event.data
        print(f"File dropped: {file_path}")
        label.config(text=f"File dropped:\n{file_path}")

    # Create a label to display the file path of the dropped file
    label = tk.Label(self.root, text="Drag and drop a file here", padx=10, pady=10)
    label.pack(pady=150, expand=True)

    # Bind the drop event to the label
    label.drop_target_register(DND_FILES)
    label.dnd_bind('<<Drop>>', drop)