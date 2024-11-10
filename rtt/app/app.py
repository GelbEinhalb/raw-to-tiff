import os
import log
import time
import config
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from converter.convert import convert

import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from typing import List


class App:

    def __init__(self, root):
        self.root = root
        self.root.geometry("850x500")
        self.root.resizable(True, False)
        self.root.overrideredirect(True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = 850
        window_height = 500
        position_top = int((screen_height / 2) - (window_height / 2))
        position_left = int((screen_width / 2) - (window_width / 2))

        self.root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

        self.x_offset = 0
        self.y_offset = 0

        # Title
        self.title_bar = tk.Frame(root, bg=config.Color.BACKGROUND_DARK, relief="raised", bd=0)
        self.title_bar.pack(fill=tk.X)
        self.title_label = tk.Label(self.title_bar, text="Raw to TIFF Converter", bg=config.Color.BACKGROUND_DARK, fg=config.Color.WHITE, padx=10)
        self.title_label.pack(side=tk.LEFT, pady=5)
        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.move_window)
        self.title_label.bind("<Button-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.close_button = tk.Button(self.title_bar, text="✕", bg=config.Color.BACKGROUND_DARK, fg=config.Color.WHITE, command=self.on_close, bd=0, padx=5, pady=5)
        self.close_button.pack(side=tk.RIGHT, padx=5)
        # Content
        self.content = tk.Frame(root, bg=config.Color.BACKGROUND)
        self.content.pack(fill="both", expand=True)
        self.console: scrolledtext.ScrolledText = scrolledtext.ScrolledText(self.content, wrap=tk.WORD, bg=config.Color.BACKGROUND, height=23, width=120, bd=0)
        self.console.config(state=tk.DISABLED)
        self.console.pack(padx=10, pady=10, fill=tk.X)
        self.label = tk.Label(self.content, text="Idle", bg=config.Color.BACKGROUND, fg=config.Color.WHITE)
        self.label.pack(pady=2)
        self.button: tk.Button = tk.Button(self.content, text="Start", command=self.start_conversion, fg=config.Color.BACKGROUND_DARK, bg=config.Color.GREEN, activeforeground=config.Color.WHITE, activebackground=config.Color.BUTTON, bd=0, highlightbackground=config.Color.BACKGROUND_DARK, highlightcolor=config.Color.BACKGROUND)
        self.button.pack(padx=10, pady=10, fill=tk.X)

        log.set_console(self.console)
        log.welcome("Click the \"Start\" button below to select a folder!", True)
        log.welcome("You can cancel the conversion at any time by closing this window.", True)
        log.info("=================================================================", True)

        self.count: int = 0
        self.start_time: float = 0
        self.image_count: int = 0
        self.lock: Lock = Lock()

        cpu_count: int = os.cpu_count()
        worker_count: int = max(1, (cpu_count - 1))
        self.executor = ThreadPoolExecutor(max_workers=worker_count)

    def increment(self) -> None:
        if self.root.winfo_exists():
            with self.lock:
                self.count += 1
                self.root.after(0, self.update_status_label)

                if self.image_count <= self.count:
                    log.info("CONVERSION COMPLETE")
                    log.info(f"Finished in {(time.time() - self.start_time):.2f} seconds")
                    self.root.after(0, lambda: self.button.config(state=tk.NORMAL))

    def update_status_label(self):
        if self.root.winfo_exists():
            self.label.config(text=f"finished {self.count} / {self.image_count} images")

    def start_conversion(self):
        self.count = 0
        self.start_time = time.time()
        self.root.after(0, lambda: self.button.config(state=tk.DISABLED))

        path: str = filedialog.askdirectory()
        destination: str = os.path.join(path, "tiff")

        log.debug(f"selected folder \"{path}\"")

        if not path or not os.path.exists(path):
            log.critical("you need to select a valid folder path")
            self.button.config(state=tk.NORMAL)
            return

        if not os.path.exists(destination):
            log.debug("creating TIFF location")
            os.mkdir(destination)
        log.set_location(destination)

        files: List[str] = os.listdir(path)
        self.image_count: int = len(files)

        Thread(target=self.background, args=(files, path, destination), daemon=True).start()

    def background(self, files, path, destination):
        for file in files:
            file_path = os.path.join(path, file)
            self.executor.submit(convert, file_path, destination, self.increment)

    def start_move(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def move_window(self, event):
        self.root.geometry(f'+{event.x_root - self.x_offset}+{event.y_root - self.y_offset}')

    def on_close(self):
        self.executor.shutdown(wait=False)
        self.root.quit()
        self.root.destroy()
