# assistant/stats.py

import os
import json

def count_classes(json_dir="detections"):
    counts = {}
    for file in os.listdir(json_dir):
        if file.endswith(".json"):
            with open(os.path.join(json_dir, file), "r") as f:
                data = json.load(f)
                for ann in data.get("annotations", []):
                    cls = ann.get("class")
                    if cls:
                        counts[cls] = counts.get(cls, 0) + 1
    return counts