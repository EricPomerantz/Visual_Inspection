import streamlit as st
from PIL import Image
import os

st.title("Visual Inspection")

# Allow user to upload multiple photos
uploaded_files = st.file_uploader("Upload one or more images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    save_dir = "uploaded_images"
    os.makedirs(save_dir, exist_ok=True)

    for uploaded_file in uploaded_files:
        # Open and display each image
        image = Image.open(uploaded_file)
        st.image(image, caption=uploaded_file.name, use_column_width=True)

        # Save each image
        save_path = os.path.join(save_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Saved to {save_path}")

