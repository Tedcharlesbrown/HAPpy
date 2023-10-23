import queue
import threading
import tkinter as tk

from encode import Encoder
from autopytoexe_path import resource_path

class HAPPY:
    def __init__(self, root, logger):
        self.root = root
        self.encode_queue = queue.Queue()
        self.encode_lock = threading.Lock()
        # self.codec_option = tk.StringVar()

        # Advanced Options
        self.advanced_options_widgets = {}
        self.placement_configs = {}

        self.setup_constants()
        self.configure_styles()
        self.setup_ui()
        self.acceptable_containers = [".mkv", ".mp4", ".mov", ".asf", ".avi", ".mxf", ".m2p", ".ps", ".ts", ".m2ts", ".mts", ".vob", ".evo", ".3gp", ".3g2", ".f4v", ".flv", ".ogv", ".ogx", ".webm", ".rmvb", ".divx", ".png", ".jpg", ".jpeg", ".tiff", ".svg"]
        self.destination_path = ""
        self.parent_folder = ""
        self.elapsed_files = 1
        self.total_files = 0
        self.console = logger



        # Encoding
        self.encoder = Encoder()
        self.overwrite_all_files = False

        # Progress bar
        self.progress_bar_update = True
        self.progress_bar_next_update = 25

        

        

    # TODO import via "from . import gui_page, filehandler_page, encode_page" - Requires changing how the functions are called

    from .gui_page import setup_constants, setup_ui, load_font, configure_styles, setup_button, setup_tree, setup_progressbar, setup_checkboxes, setup_radio, update_progress_text, console_log_progress, trigger_overwrite_popup, handle_checkbox_toggle
    from .filehandler_page import open_file_or_folder_dialog, handle_input_drop, display_input_tree, populate_file_tree, display_destination_folder, gather_files_for_encode, clear_selection, remove_file_from_tree, check_file_tree
    from .encode_page import on_encode_click, send_to_encoder, encoder_worker, run_encoder