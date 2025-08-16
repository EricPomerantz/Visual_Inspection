# utils/file_ops.py

import os
import json

def load_json(path):
    with open(path, "r") as f:
        return json.load(f)

def save_json(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def clear_folder(folder_path, extensions=None):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for file in os.listdir(folder_path):
        if extensions is None or any(file.endswith(ext) for ext in extensions):
            os.remove(os.path.join(folder_path, file))