# py
import os
from enum import Enum
# flet
# third
# own

class RenameTypes(Enum):
    CHANGE = "Change"
    PREFIX = "Prefix"

def rename_file(input_folder, option: RenameTypes, value):
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename).replace("\\", "/")
        if os.path.isfile(file_path):
            new_file_name = ""
            if option == RenameTypes.CHANGE:
                new_file_name = filename.replace(value[0], value[1])
            else: # Prefix
                new_file_name = f"{value}_{filename}"
            new_file_path = os.path.join(input_folder, new_file_name).replace("\\", "/")
            os.rename(file_path, new_file_path)

# input_folder = "./assets/files/Documents"

# rename_file(input_folder, RenameTypes.CHANGE, ["prefix_", ""])
# rename_file(input_folder, RenameTypes.PREFIX, "prefix")