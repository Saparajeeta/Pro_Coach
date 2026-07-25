import streamlit as st
from streamlit_calendar import calendar
import json

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import custom_style
custom_style.apply_custom_style()

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()

from Homepage import set_sidebar_visibility

set_sidebar_visibility(st.session_state.get("authentication_status"))

st.title("Workout Calendar")

transferred_value = st.session_state.get("transferred_variable")

mode = st.selectbox(
    "Calendar Mode:",
    (
        "daygrid",
        "timegrid",
        "timeline",
        "resource-daygrid",
        "resource-timegrid",
        "resource-timeline",
        "list",
        "multimonth",
    ),
)

if transferred_value is None:
    events = [
        {
            "title": "Workout Session",
            "start": "2026-05-08",
            "end": "2026-05-08",
            "color": "#FF4B4B",
        }
    ]
elif isinstance(transferred_value, str):
    try:
        events = json.loads(transferred_value)
    except json.JSONDecodeError:
        events = []
else:
    events = transferred_value

calendar_resources = [
    {"id": "a", "building": "Building A", "title": "Room A"},
    {"id": "b", "building": "Building A", "title": "Room B"},
    {"id": "c", "building": "Building B", "title": "Room C"},
    {"id": "d", "building": "Building B", "title": "Room D"},
    {"id": "e", "building": "Building C", "title": "Room E"},
    {"id": "f", "building": "Building C", "title": "Room F"},
]

calendar_options = {
    "editable": True,
    "navLinks": True,
    "resources": calendar_resources,
    "selectable": True,
}

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-05-01",
            "initialView": "resourceDayGridDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
            },
            "initialDate": "2026-05-01",
            "initialView": "resourceTimelineDay",
            "resourceGroupField": "building",
        }
    elif mode == "resource-timegrid":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-05-01",
            "initialView": "resourceTimeGridDay",
            "resourceGroupField": "building",
        }
else:
    if mode == "daygrid":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridDay,dayGridWeek,dayGridMonth",
            },
            "initialDate": "2026-05-01",
            "initialView": "dayGridMonth",
        }
    elif mode == "timegrid":
        calendar_options = {
            **calendar_options,
            "initialView": "timeGridWeek",
        }
    elif mode == "timeline":
        calendar_options = {
            **calendar_options,
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "timelineDay,timelineWeek,timelineMonth",
            },
            "initialDate": "2026-05-01",
            "initialView": "timelineMonth",
        }
    elif mode == "list":
        calendar_options = {
            **calendar_options,
            "initialDate": "2026-05-01",
            "initialView": "listMonth",
        }
    elif mode == "multimonth":
        calendar_options = {
            **calendar_options,
            "initialView": "multiMonthYear",
        }

state = calendar(
    events=events,
    options=calendar_options,
    custom_css="""
    .fc { background-color: #1E1E1E; color: white; border-radius: 10px; padding: 10px; }
    .fc-theme-standard td, .fc-theme-standard th { border: 1px solid #444; }
    .fc-col-header-cell-cushion { color: #1E88E5 !important; font-weight: bold; }
    .fc-daygrid-day-number { color: #FFF !important; }
    .fc-event-title { color: black; font-weight: bold; }
    .fc-event-past { opacity: 0.5; }
    .fc-event-time { font-style: italic; color: #333; }
    .fc-toolbar-title { font-size: 2rem !important; color: #FFF; }
    .fc-button-primary { background-color: #1E88E5 !important; border-color: #1E88E5 !important; }
    """,
    key=mode,
)

if state and state.get("eventsSet") is not None:
    st.session_state["events"] = state["eventsSet"]

st.divider()

st.markdown(
    """
    <style>
    .challenge-box {
        background: linear-gradient(135deg, #FF4B4B, #1E88E5);
        border-radius: 10px;
        padding: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    .challenge-box h2 { color: white; margin:0; }
    </style>
    <div class="challenge-box">
        <h2>🔥 Today's Daily Challenge</h2>
        <p style='font-size:1.2rem; margin-top:10px;'>Complete <b>50 Push-ups</b> in a single session to earn <b>500 XP</b>!</p>
    </div>
    """, unsafe_allow_html=True
)

st.write("")
with st.expander("API reference"):
    st.help(calendar)