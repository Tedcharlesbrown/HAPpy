import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

def drop(event):
    """Callback function when a folder is dropped."""
    widget_name = str(event.widget)
    if widget_name == ".!label":
        display_file_tree(event.data)
    elif widget_name == ".!label2":
        display_destination_folder(event.data)
    elif widget_name.startswith(".!treeview"):
        display_file_tree(event.data)
    elif widget_name.startswith(".!label3"):  # Assuming the name generated for destination_label is .!label3
        display_destination_folder(event.data)



def open_folder_dialog(event):
    widget_name = str(event.widget)
    folder_path = filedialog.askdirectory()
    if widget_name == ".!label":
        if folder_path:
            display_file_tree(folder_path)
    elif widget_name == ".!label2":
        if folder_path:
            display_destination_folder(folder_path)

def display_file_tree(folder_path):
    """Displays the file tree of the specified folder in the Treeview."""
    for i in tree.get_children():
        tree.delete(i)

    parent_item = tree.insert("", "end", text=folder_path, open=True)
    populate_tree(parent_item, folder_path)

def display_destination_folder(folder_path):
    """Displays the selected destination folder."""
    destination_label.config(text=folder_path)

def populate_tree(parent, folder_path):
    """Recursively populates the Treeview with the file structure."""
    for entry in os.listdir(folder_path):
        entry_path = os.path.join(folder_path, entry)
        if os.path.isdir(entry_path):
            child_item = tree.insert(parent, "end", text=entry)
            populate_tree(child_item, entry_path)
        else:
            tree.insert(parent, "end", text=entry)

root = TkinterDnD.Tk()
root.title("HAP.py")
root.geometry("800x600")
root.configure(bg="#2E2E2E")  # Dark background color

# Dark mode styling
style = ttk.Style(root)
style.theme_use("default")
style.configure("TLabel", background="#2E2E2E", foreground="#FFFFFF")
style.configure("TButton", background="#2E2E2E", foreground="#FFFFFF", relief="flat")
style.map("TButton", background=[('pressed', '#555555'), ('active', '#666666')])
style.configure("Treeview", background="#333333", foreground="#FFFFFF", fieldbackground="#333333")
style.configure("Treeview.Heading", background="#555555", foreground="#FFFFFF")

# Configure the styling for the destination label
style.configure("Destination.TLabel", 
                background="#333333",    # Background color
                foreground="#FFFFFF",    # Foreground color (text color)
                # font=('Arial', 12),     # Font and size
                padding=10,              # Padding around the text
                relief="sunken")          # Border type

style.configure("TCheckbutton", background="#2E2E2E", foreground="#FFFFFF", relief="flat")
style.map("TCheckbutton", background=[('active', '#2E2E2E')], indicatorcolor=[("selected", "#555555")], indicatorrelief=[('pressed', 'sunken'), ('!pressed', 'raised')])
style.configure("TCheckbutton", font = 100)  # You can adjust this size as needed

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


# Source Drag and Drop Area
drop_area = tk.Label(root, bg='#555555', fg='#FFFFFF', relief="raised", text="Drop a source folder here")
drop_area.place(x=20, y=80, width=350, height=60)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)
drop_area.bind('<Button-1>', open_folder_dialog)

# Treeview for displaying the file structure of the source
tree = ttk.Treeview(root)
tree.place(x=20, y=150, width=350, height=300)  # Setting an absolute width and relative height to fill vertically
tree['show'] = 'tree'

# Register Treeview as drop target and bind drop event

tree.drop_target_register(DND_FILES)
tree.dnd_bind('<<Drop>>', drop)

# Insert default values
parent = tree.insert("", "end", text="No files selected")

# Destination Drag and Drop Area
destination_drop_area = tk.Label(root, bg='#555555', fg='#FFFFFF', relief="raised", text="Drop a destination folder here")
destination_drop_area.place(x=20, y=470, width=350, height=60)
destination_drop_area.drop_target_register(DND_FILES)
destination_drop_area.dnd_bind('<<Drop>>', drop)
destination_drop_area.bind('<Button-1>', open_folder_dialog)

# Frame to display the selected destination folder
destination_label = ttk.Label(root, text="No destination selected", wraplength=300, style="Destination.TLabel")
destination_label.place(x=20, y=540, width=350, height=40)
destination_label.drop_target_register(DND_FILES)
destination_label.dnd_bind('<<Drop>>', drop)
destination_label.bind('<Button-1>', open_folder_dialog)


# IntVar to hold the state of the checkbutton (1 for checked, 0 for unchecked)
var_destination_match_source = tk.IntVar()
var_append_hap = tk.IntVar()
var_create_proxys = tk.IntVar()
var_create_proxys_only = tk.IntVar()
var_create_thumbnails = tk.IntVar()
var_create_thumbnails_only = tk.IntVar()
var_advanced_options = tk.IntVar()

# Create the checkbutton
btn_destination_match_source = ttk.Checkbutton(root, text="Destination same as Source", variable=var_destination_match_source)
btn_destination_match_source.place(x=450, y=80)

btn_append_hap = ttk.Checkbutton(root, text="Append HAP to filename (preserves version)", variable=var_append_hap)
btn_append_hap.place(x=450, y=120)

btn_create_proxys = ttk.Checkbutton(root, text="Create proxys", variable=var_create_proxys)
btn_create_proxys.place(x=450, y=160)
btn_create_proxys_only = ttk.Checkbutton(root, text="Create proxys only", variable=var_create_proxys_only)
btn_create_proxys_only.place(x=470, y=180)

btn_create_thumbnails = ttk.Checkbutton(root, text="Create thumbnails", variable=var_create_thumbnails)
btn_create_thumbnails.place(x=450, y=220)
btn_create_thumbnails_only = ttk.Checkbutton(root, text="Create thumbnails only", variable=var_create_thumbnails_only)
btn_create_thumbnails_only.place(x=470, y=240)

btn_advanced_options = ttk.Checkbutton(root, text="Advanced Codec Options", variable=var_advanced_options)
btn_advanced_options.place(x=450, y=300)

options = ["HAP", "HAP Alpha", "HAP Q", "HAP Q Alpha", "HAP Alpha Only"]
codec_option = tk.StringVar()  # To store the selected option

dropdown = ttk.Combobox(root, textvariable=codec_option, state='readonly')
dropdown['values'] = options  # Setting the options
dropdown.current(1)  # Set the default value as the first option
dropdown.place(x=470, y=325)

# ----------------------------- state controller ----------------------------- #
btn_create_proxys_only['state'] = 'disabled'
btn_create_thumbnails_only['state'] = 'disabled'

root.mainloop()
