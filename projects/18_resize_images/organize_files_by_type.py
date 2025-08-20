# py
import os
import shutil
# flet
# third
# own

file_types = {
    'Images': ['.jpeg', '.jpg', '.png', '.gif'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov'],
    'Documents': ['.pdf', '.docx', '.txt'],
    'DataSets': ['.xlsx', '.csv', '.sav'],
    'Compresseds': ['.zip', '.rar'],
    "Frontend": ['.html', '.css', '.js']
}

def organize_folder(folder):    
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename).replace("\\", "/")
        # print(file_path)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            # print(ext)
            for folder_name, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(folder, folder_name)
                    # print(target_folder)
                    os.makedirs(target_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(target_folder, filename).replace("\\", "/"))
                    # print(f"File {filename} moveded to {folder_name}.")