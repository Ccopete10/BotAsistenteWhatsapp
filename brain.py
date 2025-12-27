def buildMessage(reminder: dict) -> str:
    return f"Recuerda {reminder['mensaje']}"

def createReminderUnique(message: str, time: str, date: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "hora": time,
        "tipo": "unico",
        "activo": True,
        "ultimaEjecucion": None,
        "fecha": date,
        "ejecutado": False
    }
    return reminder

def createReminderDaily(message: str, time: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "hora": time,
        "tipo": "diario",
        "activo": True,
        "ultimaEjecucion": None, 
    }
    return reminder

def createReminderFrequent(message: str, frecuency: int, timeStart: str, timeEnd: str) -> dict:
    reminder = {
        "id": None,
        "mensaje": message,
        "intervaloMinutos": frecuency,
        "horaInicio": timeStart,
        "horaFin": timeEnd,
        "tipo": "frecuente",
        "activo": True,
        "ultimaEjecucion": None, 
    }
    return reminder