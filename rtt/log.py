import os
import config
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
            _Log.console.tag_config("WELCOME", foreground=config.Color.GREEN, font=("TkDefaultFont", 12, "bold"))
            _Log.console.tag_config("DEBUG", foreground=config.Color.WHITE)
            _Log.console.tag_config("INFO", foreground=config.Color.GREEN)
            _Log.console.tag_config("WARNING", foreground=config.Color.ORANGE)
            _Log.console.tag_config("ERROR", foreground=config.Color.RED)
            _Log.console.tag_config("CRITICAL", foreground=config.Color.RED)

    @staticmethod
    def _write_to_console(text: str, level: str, hide_info: bool = False) -> None:

        date_str: datetime.datetime.now = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
        final: str = f"[{level}] ({date_str}): {text}" if not hide_info else text

        if _Log.console is not None:
            _Log.console.config(state=tk.NORMAL)
            _Log.console.insert(tk.END, final + "\n", level)
            _Log.console.see(tk.END)
            _Log.console.config(state=tk.DISABLED)


        if _Log.location is None:
            _Log.cache.append(final)
            return

        with open(_Log.location, "a") as file:
            file.write(final + "\n")

    @staticmethod
    def write(text: str, level: str, hide_info: bool = False) -> None:
        _Log.console.after(0, lambda: _Log._write_to_console(text, level, hide_info))


def set_location(path: str) -> None:
    _Log.location = os.path.join(path, "log.txt")

def set_console(console: scrolledtext.ScrolledText) -> None:
    if _Log.console is None:
        _Log.console = console
        _Log.initialize_tags()

def welcome(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "WELCOME", hide_info)

def debug(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "DEBUG", hide_info)

def info(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "INFO", hide_info)

def warning(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "WARNING", hide_info)

def error(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "ERROR", hide_info)

def critical(text: str, hide_info: bool = False) -> None:
    _Log.write(text, "CRITICAL", hide_info)

