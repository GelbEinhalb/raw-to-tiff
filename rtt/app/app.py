import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

import log


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Camera Raw to Tiff")
        self.root.geometry("600x400")
        self.root.resizable(True, False)

        self.console: scrolledtext.ScrolledText = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=120)
        self.console.config(state=tk.DISABLED)
        self.console.pack(padx=10, pady=10, fill=tk.X)
        log.set_console(self.console)

        self.button: tk.Button = tk.Button(root, text="Start", command=self.convert)
        self.button.pack(padx=10, pady=10, fill=tk.X)


    def convert(self) -> None:
        log.debug("test")


if __name__ == "__main__":
    rt = tk.Tk()
    app = App(rt)

    rt.mainloop()