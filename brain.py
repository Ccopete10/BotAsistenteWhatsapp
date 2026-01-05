from utils.text_utils import normalize_text
from intent_detector import detect_intent
from state_manager import load_state, save_state, reset_state
from reminder_factory import create_reminder_unique, create_reminder_daily, create_reminder_frequent
import sender

def build_message(reminder: dict) -> str:
    return f"Recuerda {reminder['mensaje']}"

def change_mode(intent: str, state: dict) -> bool:
    if intent == "create_reminder":
        state["mode"] = "create_reminder"
        state["step"] = "ask_type"
        return True
    
    elif intent == "edit_reminder":
        state["mode"] = "edit_reminder"
        state["step"] = "ask_id"
        return True
    
    elif intent == "delete_reminder":
        state["mode"] = "delete_reminder"
        state["step"] = "ask_id"
        return True
    
    return False

def handle_create_reminder(text: str, state: dict) -> str:
    
    return "en proceso"
        

def process_message(message: str) -> None:
    text = normalize_text(message)
    state = load_state()
    
    # Bot en espera -> detecta intención
    if state["mode"] == "idle":
        intent = detect_intent(text)
        changed = change_mode(intent, state)
        
        if not changed:
            sender.send_message("No entendi lo que quieres hacer")
            return
        
        save_state(state)
        
        if state["mode"] == "create_reminder":
            sender.send_message("¿Qué tipo de recordatorio quieres que te cree? ¿Unico, diario o frecuente?")
        
        elif state["mode"] == "edit_reminder":
            sender.send_message("¿Qué recordatorio deseas editar?")
        
        elif state["mode"] == "delete_reminder":
            sender.send_message("¿Qué recordatorio deseas eliminar?")
        
        return
    
    # Continuacion de flujos
    elif state["mode"] == "create_reminder":
        "dsfsfs"
        
    elif state["mode"] == "edit_reminder":
        "sfsfs"
        
    elif state["mode"] == "delete_reminder":
        "sfsfs"