# detection/detector.py

import os
from utils.file_ops import load_json
from config import YOLO_JSON_DIR, CONFIDENCE_THRESHOLD

def filter_detections_by_class(class_names):
    filtered = []
    for file in os.listdir(YOLO_JSON_DIR):
        if file.endswith(".json"):
            data = load_json(os.path.join(YOLO_JSON_DIR, file))
            matches = [
                ann for ann in data.get("annotations", [])
                if ann["class"] in class_names and ann["confidence"] >= CONFIDENCE_THRESHOLD
            ]
            if matches:
                filtered.append((file, matches))
    return filtered