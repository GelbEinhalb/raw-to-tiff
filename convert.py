import os
from PIL import Image


def is_raw_file(filepath, destination, add_text):
    raw_extensions = ('.cr2', '.nef', '.arw', '.dng', '.raw')
    is_raw = filepath.lower().endswith(raw_extensions)
    if not is_raw:
        add_text(f"[INFO] skipping \"{filepath}\"", destination)
    return is_raw


def convert(filepath, destination, add_text):
    if is_raw_file(filepath, destination, add_text):
        add_text(f"[INFO] converting \"{filepath}\" to tiff", destination)
        with Image.open(filepath) as img:
            tiff_path = os.path.join(destination, os.path.splitext(os.path.basename(filepath))[0] + '.tiff')
            img.save(tiff_path, format='TIFF', compression='tiff_lzw')
