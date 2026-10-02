from config.actions import ACTION_CANCEL, ACTION_CREATE, ACTION_LEAVE
from config.messages import GREETING_MESSAGE, HIBERNATION_MESSAGE, OPTIONS_LIST
from utils.text_utils import normalize_text
from intent_detector import detect_intent
from state_manager import load_state, save_state, reset_state
from reminder_factory import create_reminder_unique, create_reminder_daily, create_reminder_frequent
from handlers import handle_create_reminder, handle_list_reminder, ask_list_option
from mode_changer import change_mode
import reminder_store
import sender


def build_message(reminder: dict) -> str:
    return f"📅 Recordatorio: {reminder['mensaje']}"

def process_message(message: str) -> str:
    raw_text = message
    normalized_text = normalize_text(message)
    state = load_state()
    reminders = reminder_store.load_reminders()
    
    if state["hibernating"]:
        state["hibernating"] = False
        state["first_message"] = True
        save_state(state)
        
    if state["first_message"]:
        state["first_message"] = False
        save_state(state)
        return GREETING_MESSAGE
    
    if normalized_text in ["cancelar", "salir", "apagar"]:
        reset_state()
        return HIBERNATION_MESSAGE
    
    # Bot en espera -> detecta intención
    if state["mode"] == "idle":
        intent = detect_intent(normalized_text)
        changed = change_mode(intent, state)
        
        if not changed:
            return "No entendi lo que quieres hacer 🤔"
        
        save_state(state)
        
        if state["mode"] == "create_reminder":
            return "⏰ ¿A qué categoria corresponde el recordatorio que quieres que te cree? ¿Únicos, Diarios o Frecuentes?"
        
        elif state["mode"] == "list_reminder":
            return "¿Qué categoria de tipos de recordatorios quieres ver? 📌 Únicos, Diarios o Frecuentes?"
        
        elif state["mode"] == "edit_reminder":
            return "✏️ ¿Qué recordatorio deseas editar?"
        
        elif state["mode"] == "delete_reminder":
            return "🗑️ ¿Qué recordatorio deseas eliminar?"
        
    # Continuacion de flujos
    elif state["mode"] == "create_reminder":
        result = handle_create_reminder(raw_text, normalized_text, state)
        
        if result == ACTION_CREATE:
            reminder_type = state["data"]["type"]
            
            if reminder_type == "unicos":
                reminder = create_reminder_unique(
                    state["data"]["message"],
                    state["data"]["time"],
                    state["data"]["date"]
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "¡Listo! Tu recordatorio fue creado con éxito 🎉"
                
            elif reminder_type == "diarios":
                reminder = create_reminder_daily(
                    state["data"]["message"],
                    state["data"]["time"]
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "¡Listo! Tu recordatorio fue creado con éxito 🎉"
                
            elif reminder_type == "frecuentes":
                reminder = create_reminder_frequent(
                    state["data"]["message"],
                    state["data"]["frequency"],
                    state["data"]["start_time"],
                    state["data"]["end_time"]    
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "¡Listo! Tu recordatorio fue creado con éxito 🎉"
            return ""
                
        elif result == ACTION_CANCEL:
            reset_state()
            return "Creacion cancelada ❌. No se guardó ningún recordatorio."
        
        return result
    
    elif state["mode"] == "list_reminder":
        
        result = handle_list_reminder(normalized_text, state, reminders)
        return result 
    
    elif state["mode"] == "after_list":

        options = ask_list_option(normalized_text, state) 

        if options == ACTION_LEAVE:
            state["mode"] = "idle"
            state["first_message"] = False
            state["hibernating"] = False
            state["step"] = None
            save_state(state)
            return GREETING_MESSAGE
        return options
        
    elif state["mode"] == "edit_reminder":
        "sfsfs"
        
    elif state["mode"] == "delete_reminder":
        "sfsfs"
    return "ocurrio un error"

try:
    while True:
        sender.send_message(process_message(input()))
        
except KeyboardInterrupt:
    reset_state()
    print("\nConversación reiniciada.")