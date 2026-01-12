from utils.text_utils import normalize_text
from intent_detector import detect_intent
from state_manager import load_state, save_state, reset_state
from reminder_factory import create_reminder_unique, create_reminder_daily, create_reminder_frequent
from utils import validators
import reminder_store
import sender

ACTION_CREATE = "CREATE"
ACTION_CANCEL = "CANCEL"

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

def handle_create_reminder(raw_text: str, normalized_text: str, state: dict) -> str:
    step = state["step"]
    
    if step == "ask_type":
        if normalized_text in ["unico", "diario", "frecuente"]:
            state["data"]["type"] = normalized_text
            state["step"] = "ask_message"
            save_state(state)
            return "¿Cual es el mensaje del recordatorio?"
        else:
            return "Tipo inválido. Usa: unico, diario o frecuente."
    
    elif step == "ask_message":
        if not validators.validate_empty_text(raw_text):
            return "El mensaje no puede estar vacio"
        elif not validators.validate_len_text(raw_text):
            return "El mensaje es demasiado largo. Usa máximo 200 caracteres"
        else:
            state["data"]["message"] = raw_text
            reminder_type = state["data"]["type"]
            
        if reminder_type == "unico" or reminder_type == "diario":
            state["step"] = "ask_time"
            save_state(state)
            return "¿A que hora? (HH:MM)"
        
        elif reminder_type == "frecuente":
            state["step"] = "ask_frequency"
            save_state(state)
            return "¿Cada cuántos minutos?"
        
    elif step == "ask_time":
        if not validators.validate_time(normalized_text):
            return "Hora inválida. Usa el formato HH:MM"
        else:
            state["data"]["time"] = normalized_text
            
        if state["data"]["type"] == "unico":
            state["step"] = "ask_date"
            save_state(state)
            return "¿Para que fecha? (YYYY-MM-DD)"
        else:
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no)"
        
    elif step == "ask_frequency":
        if not validators.validate_frequency(normalized_text):
            return "Dato no válido. Ingresa un número entre 1 y 1440 minutos"
        else:
            state["data"]["frequency"] = normalized_text 
            state["step"] = "ask_range"
            save_state(state)
            return "¿Indica rango horario: inicio-fin (HH:MM - HH:MM)"
        
    elif step == "ask_date":
        if not validators.validate_date(normalized_text):
            return "Dato no válido. Usa el formato YYYY-MM-DD"
        else:
            state["data"]["date"] = normalized_text
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no)"
    
    elif step == "ask_range":
        range_result = validators.validate_time_range(normalized_text)
        
        if not range_result:
            return "Dato no válido. Usa el formato HH:MM - HH:MM"
        else:
            start_time, end_time = range_result
            
            state["data"]["start_time"] = start_time
            state["data"]["end_time"] = end_time
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no)"
        
    elif step == "confirm":
        if normalized_text == "si":
            return ACTION_CREATE
        elif normalized_text == "no":
            return ACTION_CANCEL
        return "Dato no válido. Usa el formato sí / no"
    return "Ocurrió un error en el flujo del recordatorio."

def process_message(message: str) -> str:
    raw_text = message
    normalized_text = normalize_text(message)
    state = load_state()
    
    # Bot en espera -> detecta intención
    if state["mode"] == "idle":
        intent = detect_intent(normalized_text)
        changed = change_mode(intent, state)
        
        if not changed:
            return "No entendi lo que quieres hacer"
        
        save_state(state)
        
        if state["mode"] == "create_reminder":
            return "¿Qué tipo de recordatorio quieres que te cree? ¿Unico, diario o frecuente?"
        
        elif state["mode"] == "edit_reminder":
            return "¿Qué recordatorio deseas editar?"
        
        elif state["mode"] == "delete_reminder":
            return "¿Qué recordatorio deseas eliminar?"
        
    # Continuacion de flujos
    elif state["mode"] == "create_reminder":
        result = handle_create_reminder(raw_text, normalized_text, state)
        
        if result == ACTION_CREATE:
            reminder_type = state["data"]["type"]
            
            if reminder_type == "unico":
                reminder = create_reminder_unique(
                    state["data"]["message"],
                    state["data"]["time"],
                    state["data"]["date"]
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "Recordatorio creado exitosamente"
                
            elif reminder_type == "diario":
                reminder = create_reminder_daily(
                    state["data"]["message"],
                    state["data"]["time"]
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "Recordatorio creado exitosamente"
                
            elif reminder_type == "frecuente":
                reminder = create_reminder_frequent(
                    state["data"]["message"],
                    state["data"]["frequency"],
                    state["data"]["start_time"],
                    state["data"]["end_time"]    
                )
                
                reminder_store.add_reminder(reminder)
                reset_state()
                return "Recordatorio creado exitosamente"
            return ""
                
        elif result == ACTION_CANCEL:
            reset_state()
            return "Creacion cancelada. No se guardó ningún recordatorio."
        
        return result
        
    elif state["mode"] == "edit_reminder":
        "sfsfs"
        
    elif state["mode"] == "delete_reminder":
        "sfsfs"
    return "ocurrio un error"


while True:
    
    xd = process_message(input())
    print(xd)
    
    if xd == "c":
        break