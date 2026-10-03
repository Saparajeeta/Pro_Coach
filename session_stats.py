import threading

_LOCK = threading.RLock()
_SESSION = {}


def _key(exercise):
    return str(exercise or "unknown")


def start(exercise):
    key = _key(exercise)
    with _LOCK:
        _SESSION[key] = {"correct": 0, "incorrect": 0, "last_correct": 0, "last_incorrect": 0, "banked_correct": 0, "banked_incorrect": 0}


def update(exercise, correct, incorrect):
    key = _key(exercise)
    with _LOCK:
        state = _SESSION.setdefault(key, {"correct": 0, "incorrect": 0, "last_correct": 0, "last_incorrect": 0, "banked_correct": 0, "banked_incorrect": 0})
        if correct < state["last_correct"]:
            state["banked_correct"] += state["last_correct"]
        if incorrect < state["last_incorrect"]:
            state["banked_incorrect"] += state["last_incorrect"]
        state["correct"] = state["banked_correct"] + correct
        state["incorrect"] = state["banked_incorrect"] + incorrect
        state["last_correct"] = correct
        state["last_incorrect"] = incorrect
        return state["correct"], state["incorrect"]


def get(exercise):
    key = _key(exercise)
    with _LOCK:
        state = _SESSION.get(key)
        if state is None:
            return {"correct": 0, "incorrect": 0}
        return {"correct": state["correct"], "incorrect": state["incorrect"]}


def reset(exercise):
    key = _key(exercise)
    with _LOCK:
        _SESSION.pop(key, None)
