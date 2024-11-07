import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Camera Raw to Tiff")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.console = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20, width=70)
        self.console.pack(padx=10, pady=10)
        self.console.config(state=tk.DISABLED)

        self.button = tk.Button(root, text="Start", command=self.convert)
        self.button.pack(pady=(0, 10))

    def convert(self) -> None:
        folder_selected = filedialog.askdirectory()
        self.add_text(f"Selected folder {folder_selected}")

    def add_text(self, text):
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, text + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)


if __name__ == "__main__":
    rt = tk.Tk()
    app = App(rt)

    app.add_text("Camera Raw to Tiff Converter!")
    app.add_text("You can select a folder using the button below.")

    rt.mainloop()
