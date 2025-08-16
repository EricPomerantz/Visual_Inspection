import streamlit as st
from PIL import Image
import os

# App title
st.title("Visual Inspection Assistant")

# Sidebar for navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose a section", ["Upload & View Image"])

# Main app functionality
if app_mode == "Upload & View Image":
    st.header("Upload an Image for Inspection")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Optionally save the image to a folder
        save_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.success(f"Image saved to {save_path}")

