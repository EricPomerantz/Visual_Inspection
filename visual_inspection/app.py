import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import cv2
import numpy as np

# Load the YOLO model
model = YOLO("yolov8n.pt")

# Set up the Streamlit UI
st.title("Visual Inspection - YOLO Detection")
st.write("Upload images for detection, filter by class and confidence, and save cropped objects.")

# Sidebar settings
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.01)
class_filter_input = st.sidebar.text_input("Filter by class (comma-separated, e.g. person,car)", "")

# Handle class filters
if class_filter_input:
    class_filters = [cls.strip().lower() for cls in class_filter_input.split(",")]
else:
    class_filters = []

# Upload multiple images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

# Ensure crops directory exists
os.makedirs("crops", exist_ok=True)

# Class names from COCO dataset
class_names = model.model.names

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"Processing {uploaded_file.name}")
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        # Run YOLO inference
        results = model(image_np)[0]

        # Draw detections
        boxes = results.boxes
        annotated_img = image_np.copy()

        for i, box in enumerate(boxes):
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            label = class_names[cls_id]

            # Check confidence and class filter
            if conf < confidence_threshold:
                continue
            if class_filters and label.lower() not in class_filters:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_img, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Crop ROI and save
            crop = image_np[y1:y2, x1:x2]
            crop_filename = f"crops/{uploaded_file.name.split('.')[0]}_crop_{i}_{label}.jpg"
            cv2.imwrite(crop_filename, cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))

        # Show annotated image
        st.image(annotated_img, caption="Detections", use_column_width=True)

        st.success(f"Processed {uploaded_file.name}. Crops saved to `crops/`.")
