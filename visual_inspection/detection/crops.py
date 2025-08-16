# detection/crops.py

import os
from PIL import Image
from config import CROPS_DIR, IMAGE_DIR
from utils.file_ops import load_json

def crop_and_save(image_name, annotations):
    image_path = os.path.join(IMAGE_DIR, image_name)
    image = Image.open(image_path)

    for i, ann in enumerate(annotations):
        box = ann["bbox"]
        cropped = image.crop((box[0], box[1], box[2], box[3]))
        crop_name = f"{os.path.splitext(image_name)[0]}_crop{i}.jpg"
        crop_path = os.path.join(CROPS_DIR, crop_name)
        cropped.save(crop_path)

def crop_all(filtered_detections):
    if not os.path.exists(CROPS_DIR):
        os.makedirs(CROPS_DIR)
    for file, anns in filtered_detections:
        image_name = file.replace(".json", ".jpg")
        crop_and_save(image_name, anns)