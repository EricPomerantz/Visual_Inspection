# Visual Inspection - YOLO Detection and Agentic Assistant

This project is a visual inspection tool that combines YOLO object detection with an Agentic AI assistant. Users can upload images, filter detection results, download cropped objects, and ask questions about the results through a natural language interface.

## Features

### YOLO Object Detection
- Upload one or multiple images (`.jpg`, `.jpeg`, `.png`)
- Filter results by:
  - Confidence threshold
  - Specific class names
- Automatically crops and saves detected objects
- Download all cropped results in a `.zip` file

### Agentic AI Assistant
- Ask questions like:
  - "Fetch latest detections"
  - "Summarize events"
  - "Report statistics"
- Backend includes:
  - JSON detection loading
  - Class statistics
  - Event summarization

### Instructions

Clone this github repository and use a web hosting service such as streamlit to host the app.

OR

Visit https://visualinspection-3ub59bwul2s47adbw6pk8z.streamlit.app/ to test live.

