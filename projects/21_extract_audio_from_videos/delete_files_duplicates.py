# py
import os
import hashlib
# flet
# third
# owm

def hash_file(filename):
    h = hashlib.md5()
    with open(filename, "rb") as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(folder):
    hashes = {}
    duplicates = []
    for dirpath, _, filenames in os.walk(folder):
        for file in filenames:
            full_path = os.path.join(dirpath, file).replace("\\","/")
            file_hash = hash_file(full_path)
            if file_hash in hashes:
                # print(full_path)
                # print(hashes[file_hash])
                duplicates.append((full_path, hashes[file_hash]))
            else:
                hashes[file_hash] = full_path
    return duplicates

def delete_file(filepath):
    try:
        os.remove(filepath)
        return True
    except Exception as _:
        return False