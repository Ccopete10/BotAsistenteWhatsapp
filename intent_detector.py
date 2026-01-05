WORDS_CREATE = ["crear", "nuevo", "agregar", "anadir", "creame"]
WORDS_EDIT= ["editar", "modificar", "cambiar"]
WORDS_DELETE = ["eliminar", "borrar", "quitar"]
WORDS_REMINDER = ["recordatorio", "reminder"]

def contains_any(text: str, words: list[str]) -> bool:
    return any(word in text for word in words)

def detect_intent(text: str) -> str:
    # text debe de venir normalizado
    
    if not contains_any(text, WORDS_REMINDER):
        return "idle"
    elif contains_any(text, WORDS_CREATE):
        return "create_reminder"
    elif contains_any(text, WORDS_EDIT):
        return "edit_reminder"
    elif contains_any(text, WORDS_DELETE):
        return "delete_reminder"
    
    return "idle"
    