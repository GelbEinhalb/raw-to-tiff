import os
import log
import time
from threading import Thread
from converter.convert import convert

import tkinter
from tkinter import scrolledtext
from tkinter import filedialog

from typing import Dict
from typing import List

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Raw to Tiff")
        self.root.geometry("600x400")
        self.root.resizable(True, False)

        # Console for logging
        self.console: scrolledtext.ScrolledText = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, height=20, width=120)
        self.console.config(state=tkinter.DISABLED)
        self.console.pack(padx=10, pady=10, fill=tkinter.X)
        log.set_console(self.console)

        # Start button
        self.button: tkinter.Button = tkinter.Button(root, text="Start", command=self.start_conversion)
        self.button.pack(padx=10, pady=10, fill=tkinter.X)

        self.label: tkinter.Label = tkinter.Label(root, text="Idle")
        self.label.pack(pady=10)


    def start_conversion(self):
        start_time: float = time.time()
        self.button.config(state=tkinter.DISABLED)

        # Select the folder and set up the destination
        folder_path: str = filedialog.askdirectory()
        destination: str = os.path.join(folder_path, "tiff")

        log.debug(f"Selected folder \"{folder_path}\"")

        if not folder_path or not os.path.exists(folder_path):
            log.error("You need to select a valid folder path")
            return

        if not os.path.exists(destination):
            log.debug("Creating TIFF location")
            os.mkdir(destination)

        files: List[str] = os.listdir(folder_path)
        file_count: int = len(files)

        for file in files:
            file_path = os.path.join(folder_path, file)

            thread: Thread = Thread(target=convert, args=(file_path, destination), daemon=True)
            thread.start()

        total_time = time.time() - start_time
        log.debug(f"Total conversion time: {total_time:.2f} seconds")
        self.button.config(state=tkinter.NORMAL)
