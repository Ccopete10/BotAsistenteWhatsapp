import re
from datetime import datetime

def validate_empty_text(raw_text: str) -> bool:
    return bool(raw_text.strip())

def validate_len_text(raw_text: str) -> bool:
    return len(raw_text) <= 200

def validate_time(normalized_text: str) -> bool:
    return bool(re.match(r"^([01]\d|2[0-3]):[0-5]\d$", normalized_text))

def validate_frequency(normalized_text: str) -> bool:
    if not normalized_text.strip().isdigit():
        return False
    
    minutes = int(normalized_text.strip())
    return 1 <= minutes <= 1440

def validate_date(normalized_text: str) -> bool:
    try:
        datetime.strptime(normalized_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time_range(normalized_text: str):
    if "-" not in normalized_text:
        return None
    
    parts = normalized_text.split("-")
    
    if len(parts) != 2:
        return None
    
    start = parts[0].strip()
    end = parts[1].strip()
    
    if not validate_time(start) or not validate_time(end):
        return None
    
    start_dt = datetime.strptime(start, "%H:%M")
    end_dt = datetime.strptime(end, "%H:%M")
    
    if start_dt >= end_dt:
        return None
    
    return [start, end]