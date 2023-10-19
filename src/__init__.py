import queue
import threading
import tkinter as tk

class HAPPY:
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

    from .gui_page import setup_ui, load_font, configure_styles, setup_button, setup_tree_input, setup_encode_buttons, setup_output_tree, setup_progressbar, setup_checkboxes, setup_dropdown
    from .filehandler_page import open_file_or_folder_dialog, display_input_tree, populate_file_tree, display_destination_folder, gather_files_for_encode
    from .encode_page import on_encode_click, send_to_encoder, encoder_worker, run_encoder