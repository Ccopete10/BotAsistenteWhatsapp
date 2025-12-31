import json
import os

STATE_PATH = os.path.join("data","conversation_state.json")
DEFAULT_STATE = {
    "mode": "idle",
    "step": None,
    "data": {}
    
}

def load_state() -> dict:
    try:
        with open(STATE_PATH, 'r', encoding= 'utf-8') as data:
            data_json = json.load(data)
        if not data_json:
            return DEFAULT_STATE.copy()
        return data_json
    except FileNotFoundError:
        return DEFAULT_STATE.copy()
    except json.JSONDecodeError:
        return DEFAULT_STATE.copy()
    except Exception:
        return DEFAULT_STATE.copy()

def save_state(conversation_state: dict) -> None:
    with open(STATE_PATH, 'w', encoding= 'utf-8') as data:
        json.dump(conversation_state, data, indent=4, ensure_ascii=False)

def reset_state() -> None:
    with open(STATE_PATH, 'w', encoding= 'utf-8') as data:
        json.dump(DEFAULT_STATE, data, indent=4, ensure_ascii=False)