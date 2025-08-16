# assistant/handler.py

from assistant.summarizer import summarize_crops
from assistant.stats import count_classes

def handle_query(query):
    query = query.lower()
    if "summary" in query:
        return summarize_crops()
    elif "statistics" in query or "count" in query:
        return count_classes()
    else:
        return {"response": "Query not recognized. Try asking for 'summary' or 'statistics'."}