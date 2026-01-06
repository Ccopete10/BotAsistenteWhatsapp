import json
import os

REMINDER_PATH = os.path.join("data","reminders.json")

def load_reminders() -> list:
    try:
        with open(REMINDER_PATH, 'r', encoding= 'utf-8') as data:
            data_json = json.load(data)
        if not data_json:
            return []
        return data_json
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_reminders(reminders: list) -> None:
    with open(REMINDER_PATH, 'w', encoding= 'utf-8') as data:
        json.dump(reminders, data, indent=4, ensure_ascii=False)

def add_reminder(reminder: dict) -> None:
    reminders = load_reminders()
    reminders.append(reminder)
    save_reminders(reminders)
