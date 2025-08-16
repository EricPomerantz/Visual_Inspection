# app.py

import streamlit as st
from detection.detector import filter_detections_by_class
from detection.crops import crop_all

st.title("Visual Inspection Assistant")

classes = st.text_input("Enter class names (comma-separated)", "car,person").split(",")

if st.button("Run Detection Filter"):
    filtered = filter_detections_by_class([cls.strip() for cls in classes])
    st.write(f"Filtered detections: {len(filtered)} files")
    crop_all(filtered)
    st.success("Crops saved!")