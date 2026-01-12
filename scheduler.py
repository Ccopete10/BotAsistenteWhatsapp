import reminder_store
import datetime as dt
import brain
import sender
import time

def time_matches(reminder: dict) -> bool:
    time_now = dt.datetime.now().strftime("%H:%M")
    
    if reminder["hora"] == time_now:
        return True
    return False

def date_matches(reminder: dict) -> bool:
    date_today = dt.date.today().strftime("%Y-%m-%d")
    
    if reminder["tipo"] == "diario":
        return True
    elif reminder["fecha"] == date_today:
        return True
    return False

def is_active(reminder: dict) -> bool:
    
    if reminder["activo"] == True:
        return True
    return False

def not_execute(reminder: dict) -> bool:
    
    if reminder["ejecutado"] == False:
        return True
    return False

def different_day(last_execute: str) -> bool: 
    date_today = dt.date.today().strftime("%Y-%m-%d")
    
    if not last_execute:
        return True
    
    last_date = last_execute.split(" ")[0]   
    return last_date != date_today

def is_in_time_range(time_start: str, time_end: str, now: str) -> bool:
    return time_start <= now <= time_end

def never_executed(last_execution) -> bool:
    return last_execution is None

def today_time_to_datetime(time_str: str):
    today = dt.datetime.now().date()
    t = dt.datetime.strptime(time_str, "%H:%M").time()
    return dt.datetime.combine(today,t)

def interval_elapsed(last_execution: str, interval: int, hora_inicio: str) -> bool:
    now = dt.datetime.now()
    
    if last_execution is None:
        last_execution_dt = today_time_to_datetime(hora_inicio)
    else:
        last_execution_dt = dt.datetime.strptime(last_execution, "%Y-%m-%d %H:%M")
        
    diff_minutes = (now - last_execution_dt).total_seconds()/60
    return diff_minutes >= interval

def can_send_frequent(reminder: dict) -> bool:
    now_time = dt.datetime.now().strftime("%H:%M")
    
    if not reminder["activo"]:
        return False
    
    if not is_in_time_range(reminder["hora_inicio"], reminder["hora_fin"], now_time):
        return False
    
    if never_executed(reminder["ultima_ejecucion"]):
        return True
    
    return interval_elapsed(reminder["ultima_ejecucion"], reminder["intervalo_minutos"], reminder["hora_inicio"])

#frecuente
#diario
#unico

def if_can_send(reminder: dict) -> bool:
    if reminder["tipo"] == "unico":
        return (is_active(reminder) and
                not_execute(reminder) and
                date_matches(reminder) and 
                time_matches(reminder))
    elif reminder["tipo"] == "diario":
        return (is_active(reminder)and
                different_day(reminder["ultima_ejecucion"]) and
                time_matches(reminder))
    elif reminder["tipo"] == "frecuente":
        return can_send_frequent(reminder)
        
    return False

while True:
    now = dt.datetime.now()
    current_minute = now.strftime("%Y-%m-%d %H:%M")
    
    reminders = reminder_store.load_reminders()
    changes = False
    
    for reminder in reminders:
        if reminder["activo"] is False:
            continue
        if reminder["ultima_ejecucion"] == current_minute:
            continue
        if if_can_send(reminder):
            #llamar funcion del brain que tenga el texto que se va a enviar
            text = brain.build_message(reminder)
            #llamar funcion del sender para enviar el mensaje a whatsapp
            sender.send_message(text)
            
            if reminder["tipo"] == "unico":
                reminder["ejecutado"] = True
            
            if reminder["tipo"] == "frecuente" and reminder["ultima_ejecucion"] in None:
                reminder["ultima_ejecucion"] = f"{now.date()} {reminder['hora_inicio']}"
            else:
                reminder["ultima_ejecucion"] = current_minute
                
            changes = True
    if changes:
        reminder_store.save_reminders(reminders)
        
    time.sleep(30)
