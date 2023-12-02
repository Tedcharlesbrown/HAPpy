'''
Copyright (C) 2023  Ted Charles Brown

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
'''

import queue
import threading
import tkinter as tk

from encode import FFMPEG
from autopytoexe_path import resource_path



class HAPpy:
    def __init__(self, root, logger):
        self.root = root
        self.encode_queue = queue.Queue()
        self.encode_lock = threading.Lock()

        # Advanced Options
        self.advanced_options_widgets = {}

        self.setup_constants()
        self.configure_styles()
        # self.setup_ui()
        self.console = logger

        self.destination_path = ""
        self.parent_folder = ""
        self.elapsed_files = 1
        self.total_files = 0

        # Progress bar
        self.progress_bar_update = True
        self.progress_bar_next_update = 25

        # Encoding
        self.encoder = FFMPEG()
        self.overwrite_all_files = False
        

    # TODO import via "from . import gui_page, filehandler_page, encode_page" - Requires changing how the functions are called

    from .gui_page import setup_constants, setup_ui, load_font, configure_styles, setup_button, setup_tree, setup_progressbar, setup_checkboxes, setup_radio, update_progress_text, console_log_progress, trigger_overwrite_popup, handle_checkbox_toggle
    from .filehandler_page import open_file_or_folder_dialog, handle_input_drop, display_input_tree, populate_file_tree, display_destination_folder, gather_files_for_encode, clear_selection, remove_file_from_tree, check_file_tree
    from .encode_page import on_encode_click, send_to_encoder, encoder_worker, run_encoder