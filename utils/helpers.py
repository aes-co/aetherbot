from datetime import datetime
import uuid

def format_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def generate_id() -> str:
    return str(uuid.uuid4())

def sanitize_text(text: str) -> str:
    return text.strip()