def change_mode(intent: str, state: dict) -> bool:
    if intent == "create_reminder":
        state["mode"] = "create_reminder"
        state["step"] = "ask_type"
        return True
    elif intent == "list_reminder":
        state["mode"] = "list_reminder"
        state["step"] = "ask_type"
        return True
    elif intent == "edit_reminder":
        state["mode"] = "edit_reminder"
        state["step"] = "ask_id"
        return True
    elif intent == "delete_reminder":
        state["mode"] = "delete_reminder"
        state["step"] = "ask_id"
        return True
    else:
        return False