# py
import os
# flet
# third
from PIL import Image
# owm

image_types = {
    "PNG": "PNG",
    "JPEG": "JPEG",
    # "JPG": "JPG",
    "WEBP": "WEBP",
    "BMP": "BMP",
    "GIF": "GIF"
}

def convert_image(path, format_output):
    origin_format_output = format_output
    
    if format_output.upper() == "JPG":
            format_output = "JPEG"
    try:
        basename = os.path.splitext(path)[0]
        with Image.open(path) as img:
            # Si la img está en modo RGBA or LA y convertimos a JPEG, convertir a RGB.
            if img.mode in ("RGBA", "LA") and format_output.upper() == "JPEG":
                img = img.convert("RGB")
            # create filename output.
            path_output = f"{basename}.{"jpg" if format_output.upper() == "JPEG" and origin_format_output.upper() == "JPG" else format_output.lower()}"
            # save image.
            img.save(path_output, format_output.upper())
    except Exception as _:
        print(f"Error la convert image.")

# img = "./assets/files/Images/test.jpeg"

# convert_image(
#     img,
#     "JPG"
# )