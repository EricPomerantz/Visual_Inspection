# visual_inspection/assistant/handler.py

from assistant.summarizer import summarize_crops
from assistant.stats import count_classes
from detection.detector import load_latest_json

import re

def extract_parameters(query):
    """
    Extract mock camera ID and date from a query string.
    Example: 'Show me data for camera 2 on 2023-08-01'
    """
    camera_match = re.search(r'camera\s*(\d+)', query)
    date_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', query)

    return {
        "camera_id": camera_match.group(1) if camera_match else None,
        "date": date_match.group(1) if date_match else None
    }

def fetch_latest_detections():
    try:
        data = load_latest_json()
        return {"detections": data}
    except Exception as e:
        return {"error": f"Could not load detections: {str(e)}"}

def summarize_events():
    return summarize_crops()

def report_statistics():
    return count_classes()

def handle_query(query):
    query = query.lower()

    if "fetch" in query and "detection" in query:
        return fetch_latest_detections()

    elif "summary" in query or "summarize" in query or "event" in query:
        return summarize_events()

    elif "statistics" in query or "count" in query:
        return report_statistics()

    else:
        return {
            "response": (
                "I'm not sure what you mean. Try asking to 'fetch latest detections', "
                "'summarize events', or 'report statistics'."
            )
        }

