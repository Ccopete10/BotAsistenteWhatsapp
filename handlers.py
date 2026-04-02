
from config.actions import ACTION_CANCEL, ACTION_CREATE
from state_manager import save_state
from utils import validators

def handle_create_reminder(raw_text: str, normalized_text: str, state: dict) -> str:
    step = state["step"]
    
    if step == "ask_type":
        if normalized_text in ["unico", "diario", "frecuente"]:
            state["data"]["type"] = normalized_text
            state["step"] = "ask_message"
            save_state(state)
            return "Escribe el mensaje del recordatorio que deseas guardar ✍️"
        else:
            return "Tipo inválido ❌. Usa: único, diario o frecuente."
    
    elif step == "ask_message":
        if not validators.validate_empty_text(raw_text):
            return "El mensaje no puede estar vacío ❌"
        elif not validators.validate_len_text(raw_text):
            return "El mensaje es demasiado largo ❌. Máximo 200 caracteres"
        else:
            state["data"]["message"] = raw_text
            reminder_type = state["data"]["type"]
            
        if reminder_type == "unico" or reminder_type == "diario":
            state["step"] = "ask_time"
            save_state(state)
            return "⏰ ¿A que hora? (HH:MM)"
        
        elif reminder_type == "frecuente":
            state["step"] = "ask_frequency"
            save_state(state)
            return "⏱️ ¿Cada cuántos minutos?"
        
    elif step == "ask_time":
        if not validators.validate_time(normalized_text):
            return "Hora inválida ❌. Usa el formato HH:MM"
        else:
            state["data"]["time"] = normalized_text
            
        if state["data"]["type"] == "unico":
            state["step"] = "ask_date"
            save_state(state)
            return "📅 ¿Para que fecha? (YYYY-MM-DD)"
        else:
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no) ✅❌"
        
    elif step == "ask_frequency":
        if not validators.validate_frequency(normalized_text):
            return "Dato no válido ❌. Ingresa un número entre 1 y 1440 minutos"
        else:
            state["data"]["frequency"] = normalized_text 
            state["step"] = "ask_range"
            save_state(state)
            return "⏰ Indica el rango horario: inicio-fin (HH:MM - HH:MM)"
        
    elif step == "ask_date":
        if not validators.validate_date(normalized_text):
            return "La fecha no es válida ❌. Usa el formato YYYY-MM-DD"
        else:
            state["data"]["date"] = normalized_text
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no) ✅❌"
    
    elif step == "ask_range":
        range_result = validators.validate_time_range(normalized_text)
        
        if not range_result:
            return "Rango horario no válido ❌. Usa el formato HH:MM - HH:MM"
        else:
            start_time, end_time = range_result
            
            state["data"]["start_time"] = start_time
            state["data"]["end_time"] = end_time
            state["step"] = "confirm"
            save_state(state)
            return "¿Confirmas la creación del recordatorio? (sí / no) ✅❌"
        
    elif step == "confirm":
        if normalized_text == "si":
            return ACTION_CREATE
        elif normalized_text == "no":
            return ACTION_CANCEL
        return "Respuesta inválida ❌. Usa sí o no"
    return "Ups 😕, ocurrió un error en el flujo de creación del recordatorio. Intenta nuevamente."

def handle_list_reminder(raw_text: str, normalized_text: str, state: dict) -> str:
    step = state["step"]
    
    if step == "ask_type":
        if normalized_text in ["unico", "diario", "frecuente"]:
            state["data"]["type"] = normalized_text
            state["step"] = "show_list"
            save_state(state)
        else:
            return "Tipo inválido ❌. Usa: único, diario o frecuente."
        
    elif step == "show_list":
        reminder_type = state["data"]["type"]
        if reminder_type == "unico": 
            
def filter_reminders_by_type(reminders: list, type: str) -> list:
    pass