import os
import time
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog

import convert


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Camera Raw to Tiff")
        self.root.geometry("600x400")
        self.root.resizable(True, False)

        self.console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=120)
        self.console.pack(padx=10, pady=10)
        self.console.config(state=tk.DISABLED)

        self.button = tk.Button(root, text="Start", command=self.convert)
        self.button.pack(pady=(0, 10))

        self.saved_logs = []

    def convert(self) -> None:
        self.button.config(state=tk.DISABLED)
        start_time = time.time()
        folder_path = filedialog.askdirectory()
        destination_path = os.path.join(folder_path, "tiff")

        self.add_text(f"[INFO] Selected folder {folder_path}")

        if folder_path == "" or not os.path.exists(folder_path):
            self.add_text(f"[ERROR] You need to select a valid folder")
            return

        if not os.path.exists(destination_path):
            os.mkdir(destination_path)

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            if os.path.isdir(file_path):
                continue

            self.add_text(f"[INFO] found \"{file_path}\"", destination_path)
            convert.convert(file_path, destination_path, self.add_text)

        end_time = time.time()
        self.add_text(f"[INFO] FINISHED IN {round(end_time - start_time, 2)} SECONDS", destination_path)

        self.button.config(state=tk.NORMAL)

    def add_text(self, text, destination=None):
        if destination is None:
            self.saved_logs.append(text)
        else:
            if len(self.saved_logs) > 0:
                self.saved_logs.append(text)
                for log in self.saved_logs:
                    self.write_log_to_file(log, destination)
                self.saved_logs.clear()
            else:
                self.write_log_to_file(text, destination)

        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)

    @staticmethod
    def write_log_to_file(text, destination):
        with open(os.path.join(destination, "log.txt"), "a") as file:
            file.write(text + "\n")


if __name__ == "__main__":
    rt = tk.Tk()
    app = App(rt)

    app.add_text("Camera Raw to Tiff Converter!")
    app.add_text("You can select a folder using the button below.")

    rt.mainloop()
