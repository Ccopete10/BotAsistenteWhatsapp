import json
import datetime as dt
import brain
import sender
import time

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

def saveChanges(reminders: list) -> None:
    routData = 'data\\reminders.json'
    
    try:
        with open(routData, 'w', encoding= 'utf-8') as data:
            json.dump(reminders, data, indent=4, ensure_ascii=False)
            print("El archivo se guardo correctamente")
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en {routData}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def timeMatches(reminder: dict) -> bool:
    timeNow = dt.datetime.now().strftime("%H:%M")
    
    if reminder["hora"] == timeNow:
        return True
    return False

def dateMatches(reminder: dict) -> bool:
    dateToday = dt.date.today().strftime("%Y-%m-%d")
    
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

def differentDay(lastExecute: str) -> bool: 
    dateToday = dt.date.today().strftime("%Y-%m-%d")
    
    if not lastExecute:
        return True
    
    lastDate = lastExecute.split(" ")[0]   
    return lastDate != dateToday

#frecuente
#diario
#unico

def ifCanSend(reminder: dict) -> bool:
    if reminder["tipo"] == "unico":
        return (isActive(reminder) and
                notExecute(reminder) and
                dateMatches(reminder) and 
                timeMatches(reminder))
    elif reminder["tipo"] == "diario":
        return (isActive(reminder)and
                differentDay(reminder["ultimaEjecucion"]) and
                timeMatches(reminder))
    return False

while True:
    now = dt.datetime.now()
    currentMinute = now.strftime("%Y-%m-%d %H:%M")
    
    reminders = readReminders()
    changes = False
    
    for reminder in reminders:
        if reminder["activo"] is False:
            continue
        if reminder["ultimaEjecucion"] == currentMinute:
            continue
        if ifCanSend(reminder):
            #llamar funcion del brain que tenga el texto que se va a enviar
            text = brain.buildMessage(reminder)
            #llamar funcion del sender para enviar el mensaje a whatsapp
            sender.sendMessage(text)
            if reminder["tipo"] == "unico":
                reminder["ejecutado"] = True
            
            reminder["ultimaEjecucion"] = currentMinute
            changes = True
    if changes:
        saveChanges(reminders)
        
    time.sleep(30)
