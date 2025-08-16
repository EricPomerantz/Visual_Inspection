# assistant/metadata.py

import os
import json
import random

PARAMETER_CHOICES = {
    "CameraID": ["Cam01", "Cam02", "Cam03"],
    "Location": ["East Gate", "Main Entrance", "Parking Lot"],
    "Date": ["2023-01-15", "2023-02-17", "2023-03-10"]
}

def generate_random_metadata():
    return {
        "CameraID": random.choice(PARAMETER_CHOICES["CameraID"]),
        "Location": random.choice(PARAMETER_CHOICES["Location"]),
        "Date": random.choice(PARAMETER_CHOICES["Date"])
    }

def save_metadata(image_name, metadata_dir="metadata"):
    if not os.path.exists(metadata_dir):
        os.makedirs(metadata_dir)
    metadata = generate_random_metadata()
    name = os.path.splitext(image_name)[0] + "_meta.json"
    with open(os.path.join(metadata_dir, name), "w") as f:
        json.dump(metadata, f, indent=4)