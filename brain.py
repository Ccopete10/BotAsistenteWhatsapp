def build_message(reminder: dict) -> str:
    return f"Recuerda {reminder['mensaje']}"

def create_reminder_unique(message: str, time: str, date: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "hora": time,
        "tipo": "unico",
        "activo": True,
        "ultima_ejecucion": None,
        "fecha": date,
        "ejecutado": False
    }
    return reminder

def create_reminder_daily(message: str, time: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "hora": time,
        "tipo": "diario",
        "activo": True,
        "ultima_ejecucion": None, 
    }
    return reminder

def create_reminder_frequent(message: str, frecuency: int, time_start: str, time_end: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "intervalo_minutos": frecuency,
        "hora_inicio": time_start,
        "hora_fin": time_end,
        "tipo": "frecuente",
        "activo": True,
        "ultima_ejecucion": None, 
    }
    return reminder