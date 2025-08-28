# py
# flet
# third
from rembg import remove # type: ignore
from PIL import Image
# own

def remove_bg_img(input_path, event_path):
    input_img = Image.open(input_path)
    output_img = remove(input_img)
    output_img.save(event_path)