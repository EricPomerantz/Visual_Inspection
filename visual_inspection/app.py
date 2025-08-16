import streamlit as st
from PIL import Image
import os
from ultralytics import YOLO
import tempfile

# Load the model once
model = YOLO("yolov8n.pt")  # Replace with your custom model if needed

st.title("Visual Inspection with YOLO")

uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    save_dir = "uploaded_images"
    os.makedirs(save_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        # Save the image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
            tmp_file.write(uploaded_file.read())
            temp_path = tmp_file.name

        # Run detection
        results = model(temp_path)

        # Save annotated result
        annotated_image_path = temp_path.replace(".jpg", "_annotated.jpg")
        for r in results:
            r.save(filename=annotated_image_path)

        # Display original and annotated image
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(temp_path), caption="Original", use_column_width=True)
        with col2:
            st.image(Image.open(annotated_image_path), caption="YOLO Detection", use_column_width=True)

        # Save permanently if desired
        final_path = os.path.join(save_dir, uploaded_file.name)
        with open(final_path, "wb") as f:
            f.write(open(temp_path, "rb").read())

