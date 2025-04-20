# utils/helpers.py

def handle_input(data, engine):
    action = data.get("action")
    if not action:
        return handle_input_error("Missing 'action'.")

    kwargs = {k: v for k, v in data.items() if k != "action"}
    return engine.run_action(action, **kwargs)

def handle_input_error(message="Invalid input."):
    return {
        "error": True,
        "message": message
    }
