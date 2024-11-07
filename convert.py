import rawpy
import imageio
import os

def is_raw_file(filepath, destination, add_text):
    raw_extensions = ('.cr2', '.nef', '.arw', '.dng', '.raw')
    is_raw = filepath.lower().endswith(raw_extensions)
    if not is_raw:
        add_text(f"[INFO] skipping \"{filepath}\"", destination)
    return is_raw

def convert(filepath, destination, add_text):
    if is_raw_file(filepath, destination, add_text):
        add_text(f"[INFO] converting \"{filepath}\" to TIFF using imageio", destination)

        with rawpy.imread(filepath) as raw:

            rgb = raw.postprocess(
                output_bps=16,
                no_auto_bright=True,
                use_camera_wb=True
            )

            tiff_path = os.path.join(destination, os.path.splitext(os.path.basename(filepath))[0] + '.tiff')

            imageio.imwrite(filepath=tiff_path, im=rgb, format='TIFF')
            add_text(f"[INFO] saved \"{tiff_path}\" as uncompressed 16-bit TIFF", destination)
