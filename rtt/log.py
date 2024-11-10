import datetime
import tkinter as tk
from tkinter import scrolledtext
from typing import List


class _Log:

    cache: List[str] = []
    location: str = None
    console: scrolledtext.ScrolledText = None

    @staticmethod
    def write(text: str) -> None:
        if _Log.console is not None:
            _Log.console.config(state=tk.NORMAL)
            _Log.console.insert(tk.END, text + "\n")
            _Log.console.see(tk.END)
            _Log.console.config(state=tk.DISABLED)

        if _Log.location is None:
            _Log.cache.append(text)
            return

        with open(_Log.location, "a") as file:
            file.write(text + "\n")


def set_location(path: str) -> None:
    _Log.location = path + "log.txt"
    for line in _Log.cache:
        _Log.write(line)

def set_console(console: scrolledtext.ScrolledText) -> None:
    _Log.console = console

# Information to help diagnose a problem
def debug(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[DEBUG] ({date_str}): {text}")

# Information about the process
def info(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[INFO] ({date_str}): {text}")

# Something doesn't seem right
def warning(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[WARNING] ({date_str}): {text}")

# Something went wrong
def error(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[ERROR] ({date_str}): {text}")

# Something went wrong, and the process was cancelled
def critical(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[CRITICAL] ({date_str}): {text}")