def record_processor_session(processor, exercise_name, username, label=None):
    return {
        "exercise": exercise_name,
        "username": username,
        "label": label,
        "processor": processor,
    }
