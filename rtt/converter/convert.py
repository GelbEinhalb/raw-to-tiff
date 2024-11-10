import rawpy
import imageio
import os
import log

def is_raw_file(path):
    raw_extensions = ('.cr2', '.nef', '.arw', '.dng', '.raw')
    is_raw = path.lower().endswith(raw_extensions)
    if not is_raw:
        log.debug(f"Skipping \"{path}\"")
    return is_raw

def convert(path, destination, increment):
    if is_raw_file(path):
        with rawpy.imread(path) as raw:
            rgb = raw.postprocess(
                output_bps=16,
                no_auto_bright=True,
                use_camera_wb=True
            )

            tiff_path = os.path.join(destination, os.path.splitext(os.path.basename(path))[0] + '.tiff')
            imageio.imwrite(uri=tiff_path, im=rgb, format='TIFF')
            log.info(f"Converted \"{path}\"")
    increment()