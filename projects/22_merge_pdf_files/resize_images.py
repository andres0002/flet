# py
import os
# flet
# third
from PIL import Image
# owm

def batch_resize(folder_in, folder_out, prefix, width, height):
    for filename in os.listdir(folder_in):
        if filename.endswith((".jpeg", ".jpg", ".png")):
            # print(os.path.join(folder_in, filename).replace("\\", "/"))
            img = Image.open(os.path.join(folder_in, filename).replace("\\", "/"))
            img = img.resize((width, height))
            # print(os.path.join(folder_out, f"resized_{filename}").replace("\\", "/"))
            img.save(os.path.join(folder_out, f"{prefix}_{width}_x_{height}_{filename}").replace("\\", "/"))

# batch_resize(
#     "./assets/files/Images",
#     "./assets/files/Images/resized_images",
#     "resized",
#     800,
#     600
# )