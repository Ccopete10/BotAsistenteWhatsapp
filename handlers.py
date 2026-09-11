
from config.actions import ACTION_CANCEL, ACTION_CREATE, ACTION_LEAVE
import reminder_store
from state_manager import save_state
from utils import validators

reminders = reminder_store.load_reminders

def handle_create_reminder(raw_text: str, normalized_text: str, state: dict) -> str:
    step = state["step"]
    
    if step == "ask_type":
        if normalized_text in ["unicos", "diarios", "frecuentes"]:
            state["data"]["type"] = normalized_text
            state["step"] = "ask_message"
            save_state(state)
            return "Escribe el mensaje del recordatorio que deseas guardar ✍️"
        else:
            return "Tipo inválido ❌. Usa: unicos, diarios o frecuentes."
    
    elif step == "ask_message":
        if not validators.validate_empty_text(raw_text):
            return "El mensaje no puede estar vacío ❌"
        elif not validators.validate_len_text(raw_text):
            return "El mensaje es demasiado largo ❌. Máximo 200 caracteres"
        else:
            state["data"]["message"] = raw_text
            reminder_type = state["data"]["type"]
            
        if reminder_type == "unicos" or reminder_type == "diarios":
            state["step"] = "ask_time"
            save_state(state)
            return "⏰ ¿A que hora? (HH:MM)"
        
        elif reminder_type == "frecuentes":
            state["step"] = "ask_frequency"
            save_state(state)
            return "⏱️ ¿Cada cuántos minutos?"
        
    elif step == "ask_time":
        if not validators.validate_time(normalized_text):
            return "Hora inválida ❌. Usa el formato HH:MM"
        else:
            state["data"]["time"] = normalized_text
            
        if state["data"]["type"] == "unicos":
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

def handle_list_reminder(normalized_text: str, state: dict, reminders: list) -> str:
    
    if state["step"] == "ask_type":
        if normalized_text in ["unicos", "diarios", "frecuentes"]:
            state["data"]["type"] = normalized_text
            state["step"] = "show_list"
            save_state(state)
        else:
            state["step"] = "ask_type"
            return "Tipo inválido ❌. Usa: Únicos, Diarios o Frecuentes."
        
    if state["step"] == "show_list":
        reminder_type = state["data"]["type"]
        filter_reminder = [x for x in reminders if x["tipo"] == reminder_type]

        if not filter_reminder:
            state["data"].clear()
            state["step"] = "ask_type"
            save_state(state)
            return f"No se encontraron recordatorios en la categoria {reminder_type}. Vuelve a elegir una categoria: Únicos, Diarios o Frecuentes"
        
        message = f"📝 Recordatorios en la categoria {reminder_type}:\n\n"

        if reminder_type == "unicos":
            for i in filter_reminder:
                message += (
                    f"• {i["mensaje"]}\n"
                    f"  Fecha: {i["fecha"]}\n"
                    f"  Hora: {i["hora"]}\n\n"
                )
            

        elif reminder_type == "diarios":
            for i in filter_reminder:
                message += (
                    f"• {i["mensaje"]}\n"
                    f"  Hora: {i["hora"]}\n\n"
                )
                
        elif reminder_type == "frecuentes":
            for i in filter_reminder:
                message += (
                    f"• {i["mensaje"]}\n"
                    f"  Intervalo de tiempo: {i["intervalo_minutos"]}\n"
                    f"  Hora inicio: {i["hora_inicio"]}\n"
                    f"  Hora fin: {i["hora_fin"]}\n"
                )
                
        state["data"].clear()
        state["step"] = "ask_list_action"
        save_state(state)
        
        return message + "\n¿Quieres salir al menu principal o listar otra categoria?"
    
    if state["step"] == "ask_list_action":
        return ask_list_action(normalized_text, state) 
    else:
        return "Vuelve a intentar tu petición de la manera correcta"

def ask_list_action(normalized_text: str, state: dict) -> str:
    
    if normalized_text in ["salir", "leave", "menu"]:
        return ACTION_LEAVE
    
    elif normalized_text in ["listar", "ver"]:
        state["step"] = "ask_type"
        save_state(state)
        return "¿Que categoria quieres ver: Únicos, Diarios o Frecuentes?"
        
    else:
        return "No entendi lo que quieres hacer, escribe: (salir, menu, listar o ver)"