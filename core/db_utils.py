import json
from datetime import datetime
from pathlib import Path


def record_processor_session(processor, exercise_name, username, label=None):
    try:
        state_tracker = processor.state_tracker
        correct = next((value for key, value in state_tracker.items() if key.endswith("_COUNT")), 0)
        incorrect = next((value for key, value in state_tracker.items() if key.startswith("IMPROPER")), 0)
        record = {
            "exercise": exercise_name,
            "username": username,
            "label": label,
            "correct": int(correct),
            "incorrect": int(incorrect),
            "timestamp": datetime.now().isoformat(),
        }
        history_path = Path("session_history.json")
        if history_path.exists():
            with history_path.open("r", encoding="utf-8") as history_file:
                history = json.load(history_file)
        else:
            history = []
        if not isinstance(history, list):
            history = []
        history.append(record)
        with history_path.open("w", encoding="utf-8") as history_file:
            json.dump(history, history_file)
        return record
    except Exception:
        return None
