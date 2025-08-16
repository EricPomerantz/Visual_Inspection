# assistant/summarizer.py

import os
import json

def summarize_crops(crop_dir="crops"):
    crop_files = [f for f in os.listdir(crop_dir) if f.endswith(".jpg")]
    return {
        "total_crops": len(crop_files),
        "examples": crop_files[:5]
    }