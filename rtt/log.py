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

        if _Log.console is not None:
            _Log.console.after(0, lambda: _Log.console.insert(tk.END, text + "\n"))


def set_location(path: str) -> None:
    _Log.location = os.path.join(path, "log.txt")
    for line in _Log.cache:
        _Log.write(line)

def set_console(console: scrolledtext.ScrolledText) -> None:
    _Log.console = console

def debug(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[DEBUG] ({date_str}): {text}")

def info(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[INFO] ({date_str}): {text}")

def warning(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[WARNING] ({date_str}): {text}")

def error(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[ERROR] ({date_str}): {text}")

def critical(text: str) -> None:
    date_str: str = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    _Log.write(f"[CRITICAL] ({date_str}): {text}")
