import streamlit as st
import pandas as pd
from PIL import Image
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
import os
from dotenv import load_dotenv
import security
import custom_style

# 1. Security Check
security.verify_integrity()

# 2. Load Environment Variables
load_dotenv()

def set_sidebar_visibility(authentication_status):
    return authentication_status

# Update the page browser tab configuration
st.set_page_config(
    layout="wide",
    page_title="🦾 The Pro Coach - AI Assistant",
    page_icon="🦾",
)

# Apply global premium styling
custom_style.apply_custom_style()

file_path = Path(__file__).parent / "hashed.pkl"

missing_env_vars = [
    name for name in ("APARA_PASS", "ADIT_PASS", "COOKIE_KEY")
    if not os.getenv(name)
]
if missing_env_vars:
    st.error("Missing APARA_PASS, ADIT_PASS or COOKIE_KEY. Create a .env file from .env.example.")
    st.stop()

users_data = {
    "usernames": {
        "aparajeeta": {
            "name": "Aparajeeta",
            "password": os.getenv("APARA_PASS")
        },
        "aditya": {
            "name": "Aditya",
            "password": os.getenv("ADIT_PASS")
        }
    }
}

with open(file_path, "rb") as f:
    hashed_passwords = pickle.load(f)

# Update the Cookie name for your official branding
authenticator = stauth.Authenticate(
    credentials=users_data,
    cookie_name="The Pro Coach AI",
    cookie_key=os.getenv("COOKIE_KEY"),
    cookie_expiry_days=30
)

authenticator.login(location="main")

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")
username = st.session_state.get("username")

if authentication_status is False:
    st.error("Usernames and passwords do not match. Please try again.")
elif authentication_status is None:
    st.error("Please enter your username and password to login.")
elif authentication_status is True:
    authenticator.logout(location="sidebar")
    st.sidebar.title(f"Welcome {name} to 🦾 The Pro Coach")

    from home_dashboard import render_home

    nav_pages = {
        "Home": [st.Page(render_home, title="Dashboard", default=True)],
        "Exercises": [
            st.Page("pages/Squat AI Trainer.py", title="Squat AI Trainer", icon="🏋️"),
            st.Page("pages/5_Pushup_AI_Trainer.py", title="Push-up AI Trainer", icon="💪"),
            st.Page("pages/Bicep Curl AI Trainer.py", title="Bicep Curl AI Trainer", icon="🏋️"),
            st.Page("pages/Lunges AI Trainer.py", title="Lunges AI Trainer", icon="🦵"),
            st.Page("pages/Tricep KickBack.py", title="Tricep KickBack", icon="💪"),
            st.Page("pages/Dumbbell Fly AI Trainer.py", title="Dumbbell Fly AI Trainer", icon="🏋️"),
            st.Page("pages/10_Overhead_Dumbbell_Shoulder_Press.py", title="Shoulder Press AI Trainer", icon="🏋️"),
            st.Page("pages/11_Standing_Lateral_Dumbbell_Raises.py", title="Lateral Raises AI Trainer", icon="🏋️"),
            st.Page("pages/12_Romanian_Deadlifts.py", title="Romanian Deadlifts AI Trainer", icon="🏋️"),
        ],
        "Yoga": [
            st.Page("pages/13_Tree_Pose.py", title="Tree Pose", icon="🧘"),
            st.Page("pages/14_Warrior_II_Pose.py", title="Warrior II Pose", icon="🧘"),
        ],
        "Sports Exercises": [
            st.Page("pages/15_Cricket_Bowling_Action.py", title="Cricket Bowling Action", icon="🏏"),
            st.Page("pages/16_Football_Kick.py", title="Football Kick", icon="⚽"),
        ],
        "Tools": [
            st.Page("pages/1_Demo.py", title="Demo", icon="🎬"),
            st.Page("pages/6_Workout_Analytics.py", title="Workout Analytics", icon="📊"),
            st.Page("pages/3_Excercises_Recommendation.py", title="Exercise Recommendation", icon="🧭"),
            st.Page("pages/4_Calendar.py", title="Calendar", icon="📅"),
            st.Page("pages/2_Methodology_and_Data.py", title="Methodology and Data", icon="📘"),
        ],
    }
    pg = st.navigation(nav_pages)
    pg.run()
