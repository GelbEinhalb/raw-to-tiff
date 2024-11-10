import os
import log
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from converter.convert import convert

import tkinter
from tkinter import scrolledtext
from tkinter import filedialog

from typing import List

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Raw to Tiff")
        self.root.geometry("800x400")
        self.root.resizable(True, False)

        # Console for logging
        self.console: scrolledtext.ScrolledText = scrolledtext.ScrolledText(root, wrap=tkinter.WORD, height=18, width=120)
        self.console.config(state=tkinter.DISABLED)
        self.console.pack(padx=10, pady=10, fill=tkinter.X)
        log.set_console(self.console)

        # Status Label
        self.label = tkinter.Label(root, text="Idle")
        self.label.pack(pady=2)

        # Start button
        self.button: tkinter.Button = tkinter.Button(root, text="Start", command=self.start_conversion)
        self.button.pack(padx=10, pady=10, fill=tkinter.X)

        self.count: int = 0
        self.start_time: float = 0
        self.image_count: int = 0
        self.lock: Lock = Lock()

    def increment(self) -> None:
        with self.lock:
            self.count += 1
            self.root.after(0, self.update_status_label)

            if self.image_count <= self.count:
                log.info("CONVERSION COMPLETE")
                log.info(f"Finished in {(time.time() - self.start_time):.2f} seconds")
                self.root.after(0, lambda: self.button.config(state=tkinter.NORMAL))

    def update_status_label(self):
        self.label.config(text=f"Finished {self.count} / {self.image_count} Images")

    def start_conversion(self):
        self.count = 0
        self.start_time = time.time()
        self.button.config(state=tkinter.DISABLED)

        path: str = filedialog.askdirectory()
        destination: str = os.path.join(path, "tiff")

        log.debug(f"Selected folder \"{path}\"")

        if not path or not os.path.exists(path):
            log.error("You need to select a valid folder path")
            self.button.config(state=tkinter.NORMAL)
            return

        if not os.path.exists(destination):
            log.debug("Creating TIFF location")
            os.mkdir(destination)
        log.set_location(destination)

        files: List[str] = os.listdir(path)
        self.image_count: int = len(files)


        Thread(target=self.background, args=(files, path, destination), daemon=True).start()

    def background(self, files, path, destination):
        with ThreadPoolExecutor(max_workers=8) as executor:
            for file in files:
                file_path = os.path.join(path, file)
                executor.submit(convert, file_path, destination, self.increment)
