import unicodedata

def normalize_text(message: str) -> str:
    text = message.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text.strip()