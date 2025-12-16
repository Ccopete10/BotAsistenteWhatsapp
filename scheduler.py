import json
import datetime as dt

def readReminders() -> list:
    routData = 'data\\reminders.json'
    
    try:
        with open(routData, 'r', encoding= 'utf-8') as data:
            dataJson = json.load(data)
        if not dataJson:
            return []
        return dataJson
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en {routData}")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo no es un JSON válido.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return []

reminders = readReminders()
timeNow = dt.datetime.now().strftime("%H:%M")
dateToday = dt.date.today().strftime("%Y-%m-%d")

def timeMatches(reminder: dict) -> bool:
    if reminder["hora"] == timeNow:
        return True
    return False

def dateMatches(reminder: dict) -> bool:
    if reminder["tipo"] == "diario":
        return True
    elif reminder["fecha"] == dateToday:
        return True
    return False

def isActive(reminder: dict) -> bool:
    if reminder["activo"] == True:
        return True
    return False

def notExecute(reminder: dict) -> bool:
    if reminder["ejecutado"] == False:
        return True
    return False

def lastDateAndTime()-> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    return now
