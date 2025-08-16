# app.py 

import os
import streamlit as st
from PIL import Image
import uuid
import json
from utils.file_ops import save_json

from assistant.metadata import simulate_metadata  # or real detector in future

st.title("Visual Inspection Assistant")

# Upload image only
st.header("1. Upload Image")

uploaded_image = st.file_uploader("Upload Image (.jpg)", type=["jpg", "jpeg"])

if uploaded_image:
    # Generate unique name
    image_id = uuid.uuid4().hex
    image_name = f"{image_id}.jpg"
    image_path = os.path.join("images", image_name)

    # Save image
    with open(image_path, "wb") as f:
        f.write(uploaded_image.read())

    # Simulate detection JSON
    json_name = f"{image_id}.json"
    json_path = os.path.join("detections", json_name)

    simulated_json = simulate_metadata(image_path)
    save_json(simulated_json, json_path)

    st.success(f"Uploaded {image_name} and generated detection data.")
    st.image(Image.open(image_path), caption="Uploaded Image", use_column_width=True)
else:
    st.info("Please upload an image to begin.")
