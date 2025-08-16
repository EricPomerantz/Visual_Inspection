# app.py

import os
import streamlit as st
from detection.detector import filter_detections_by_class
from detection.crops import crop_all
from utils.file_ops import save_json
from PIL import Image
import uuid

st.title("Visual Inspection Assistant")

# Upload image and JSON pair
st.header("1. Upload Image and Detection JSON")

uploaded_image = st.file_uploader("Upload Image (.jpg)", type=["jpg", "jpeg"])
uploaded_json = st.file_uploader("Upload Detection JSON (.json)", type=["json"])

if uploaded_image and uploaded_json:
    # Save both to the proper folders
    image_name = f"{uuid.uuid4().hex}.jpg"
    json_name = os.path.splitext(image_name)[0] + ".json"

    image_path = os.path.join("images", image_name)
    json_path = os.path.join("detections", json_name)

    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    import json
    save_json(json.load(uploaded_json), json_path)

    st.success(f"Saved: {image_name} and {json_name}")
else:
    st.info("Please upload both an image and its detection JSON file.")
