import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import cv2
import numpy as np
import zipfile
import io

# 👇 Agentic AI Imports
from assistant.handler import handle_query

# Load YOLO model
model = YOLO("yolov8n.pt")
class_names = model.model.names

# Streamlit UI
st.title("Visual Inspection - YOLO Detection")
st.write("Upload images, filter by confidence and class, and download cropped objects.")

# Sidebar controls
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.01)
class_filter_input = st.sidebar.text_input("Filter by class (comma-separated)", "")

# Parse class filters
class_filters = [cls.strip().lower() for cls in class_filter_input.split(",") if cls.strip()] if class_filter_input else []

# Upload images
uploaded_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Clear crops folder
os.makedirs("crops", exist_ok=True)
for f in os.listdir("crops"):
    os.remove(os.path.join("crops", f))

# Store cropped image paths
all_crop_paths = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        results = model(image_np)[0]
        boxes = results.boxes

        valid_detections = []
        for i, box in enumerate(boxes):
            cls_id = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            label = class_names[cls_id]

            if conf < confidence_threshold:
                continue
            if class_filters and label.lower() not in class_filters:
                continue

            # This detection is valid
            valid_detections.append((box, label, conf, i))

        # Only show image if valid detections exist
        if valid_detections:
            annotated_img = image_np.copy()

            for box, label, conf, idx in valid_detections:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_img, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Crop and save
                crop = image_np[y1:y2, x1:x2]
                crop_filename = f"crops/{uploaded_file.name.split('.')[0]}_crop_{idx}_{label}.jpg"
                cv2.imwrite(crop_filename, cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
                all_crop_paths.append(crop_filename)

            st.subheader(f"Detections in {uploaded_file.name}")
            st.image(annotated_img, caption="Annotated Image", use_container_width=True)

    # Show download button if crops exist
    if all_crop_paths:
        # Create in-memory zip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for path in all_crop_paths:
                zipf.write(path, arcname=os.path.basename(path))
        zip_buffer.seek(0)

        st.success(f"{len(all_crop_paths)} cropped objects saved.")
        st.download_button("Download All Crops as ZIP", zip_buffer, file_name="crops.zip", mime="application/zip")
    else:
        st.warning("No valid detections found for the current filters.")

# 🧠 Agentic AI Assistant Section
st.subheader("🧠 Agentic Assistant")
query = st.text_input("Ask something like: 'fetch latest detections', 'summarize events', or 'report statistics'")

if query:
    response = handle_query(query)
    st.write("### Assistant Response")
    st.json(response)
