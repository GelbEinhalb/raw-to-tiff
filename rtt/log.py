import os
import datetime
import tkinter as tk
from tkinter import scrolledtext
from typing import List

class _Log:
    cache: List[str] = []
    location: str = None
    console: scrolledtext.ScrolledText = None

    @staticmethod
    def initialize_tags():
        if _Log.console is not None:
            _Log.console.tag_config("WELCOME", foreground="purple", font=("TkDefaultFont", 12, "bold"))
            _Log.console.tag_config("DEBUG", foreground="black")
            _Log.console.tag_config("INFO", foreground="dark green", font=("TkDefaultFont", 10, "bold"))
            _Log.console.tag_config("WARNING", foreground="orange")
            _Log.console.tag_config("ERROR", foreground="red", font=("TkDefaultFont", 11, "bold"))
            _Log.console.tag_config("CRITICAL", foreground="dark red", font=("TkDefaultFont", 11, "bold"))

    @staticmethod
    def write(text: str, level: str = "INFO") -> None:
        # Insert text with the level tag directly if called from the main thread
        if _Log.console is not None:
            _Log.console.config(state=tk.NORMAL)
            _Log.console.insert(tk.END, text + "\n", level)
            _Log.console.see(tk.END)
            _Log.console.config(state=tk.DISABLED)

        # Write to log file
        if _Log.location is None:
            _Log.cache.append(text)
            return

        with open(_Log.location, "a") as file:
            file.write(text + "\n")

    @staticmethod
    def write_to_console(text: str, level: str) -> None:
        if _Log.console is not None:
            _Log.console.after(0, lambda: _Log.write(text, level))


def set_location(path: str) -> None:
    _Log.location = os.path.join(path, "log.txt")

def set_console(console: scrolledtext.ScrolledText) -> None:
    if _Log.console is None:
        _Log.console = console
        _Log.initialize_tags()

def welcome(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[WELCOME] ({date_str}): {text}", "WELCOME")

def debug(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[DEBUG] ({date_str}): {text}", "DEBUG")

def info(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[INFO] ({date_str}): {text}", "INFO")

def warning(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[WARNING] ({date_str}): {text}", "WARNING")

def error(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[ERROR] ({date_str}): {text}", "ERROR")

def critical(text: str) -> None:
    date_str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write_to_console(f"[CRITICAL] ({date_str}): {text}", "CRITICAL")

