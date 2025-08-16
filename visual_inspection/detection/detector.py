# visual_inspection/detection/detector.py

import os
import json
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

def load_latest_json():
    """
    Loads and returns the latest JSON file from YOLO_JSON_DIR.
    """
    json_files = [f for f in os.listdir(YOLO_JSON_DIR) if f.endswith(".json")]
    if not json_files:
        return {}

    latest_file = max(json_files, key=lambda f: os.path.getmtime(os.path.join(YOLO_JSON_DIR, f)))
    with open(os.path.join(YOLO_JSON_DIR, latest_file), "r") as f:
        return json.load(f)
