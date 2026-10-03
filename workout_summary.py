import json
from datetime import datetime

import streamlit as st

import session_stats
from suggestions import build_suggestions


def start_workout(exercise):
    started_key = f"workout_started_{exercise}"
    if started_key not in st.session_state:
        st.session_state[started_key] = datetime.now().isoformat()
        session_stats.start(exercise)
    return st.session_state[started_key]


def render_finish_workout(exercise, started_at, correct_available=True, incorrect_available=True):
    if not st.button("Finish workout", key=f"finish_workout_{exercise}"):
        return

    counts = session_stats.get(exercise)
    if correct_available:
        st.write(f"Correct reps: {counts['correct']}")
    else:
        st.write("Correct reps: Not tracked")
    if incorrect_available:
        st.write(f"Incorrect reps: {counts['incorrect']}")
    else:
        st.write("Incorrect reps: Not tracked")

    mistakes = []
    try:
        with open("session_mistakes.json", "r", encoding="utf-8") as mistake_file:
            records = json.load(mistake_file)
        session_start = datetime.fromisoformat(started_at)
        for record in records:
            try:
                if datetime.fromisoformat(record["time"]) >= session_start:
                    mistakes.append(record["mistake"])
            except (KeyError, TypeError, ValueError):
                continue
    except (OSError, TypeError, ValueError):
        pass

    st.write("Mistakes logged this session:")
    if mistakes:
        for mistake in mistakes:
            st.write(f"- {mistake}")
    else:
        st.write("None logged in this session.")

    suggestions = build_suggestions(exercise, counts["correct"], counts["incorrect"], mistakes)
    st.write("Suggestions:")
    for tip in suggestions["tips"]:
        st.write(f"- {tip}")
    for follow_up in suggestions["follow_ups"]:
        st.write(follow_up["reason"])
        st.page_link(follow_up["page"], label=follow_up["label"])
    st.write(suggestions["safety"])