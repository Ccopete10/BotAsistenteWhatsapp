import unicodedata

WORDS_CREATE = ["crear", "nuevo", "agregar", "anadir", "creame"]
WORDS_EDIT= ["editar", "modificar", "cambiar"]
WORDS_DELETE = ["eliminar", "borrar", "quitar"]
WORDS_REMINDER = ["recordatorio", "reminder"]

def normalize_text(message: str) -> str:
    text = message.lower()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text.strip()

def contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)

def detect_intent(message: str) -> str:
    text = normalize_text(message)
    
    if not contains_any(text, WORDS_REMINDER):
        return "idle"
    elif contains_any(text, WORDS_CREATE):
        return "create_reminder"
    elif contains_any(text, WORDS_EDIT):
        return "edit_reminder"
    elif contains_any(text, WORDS_DELETE):
        return "delete_reminder"
    
    return "idle"
    