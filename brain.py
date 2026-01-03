import reminder_factory as factory

def build_message(reminder: dict) -> str:
    return f"Recuerda {reminder['mensaje']}"

