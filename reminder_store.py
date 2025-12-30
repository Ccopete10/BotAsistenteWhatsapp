import json

def read_reminders() -> list:
    rout_data = 'data\\reminders.json'
    
    try:
        with open(rout_data, 'r', encoding= 'utf-8') as data:
            data_json = json.load(data)
        if not data_json:
            return []
        return data_json
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en {rout_data}")
        return []
    except json.JSONDecodeError:
        print("Error: El archivo no es un JSON válido.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return []

def save_changes(reminders: list) -> None:
    rout_data = 'data\\reminders.json'
    
    try:
        with open(rout_data, 'w', encoding= 'utf-8') as data:
            json.dump(reminders, data, indent=4, ensure_ascii=False)
            print("El archivo se guardo correctamente")
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró en {rout_data}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")