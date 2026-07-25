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

users_data = {
    "usernames": {
        "aparajeeta": {
            "name": "Aparajeeta",
            "password": os.getenv("APARA_PASS", "fallback_pass")
        },
        "aditya": {
            "name": "Aditya",
            "password": os.getenv("ADIT_PASS", "fallback_pass")
        }
    }
}

with open(file_path, "rb") as f:
    hashed_passwords = pickle.load(f)

# Update the Cookie name for your official branding
authenticator = stauth.Authenticate(
    credentials=users_data,
    cookie_name="The Pro Coach AI",
    cookie_key=os.getenv("COOKIE_KEY", "fallback_cookie_key"),
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
    
    # Update the sidebar welcome message
    st.sidebar.title(f"Welcome {name} to 🦾 The Pro Coach")

    def initial_state():
        if 'df' not in st.session_state:
            st.session_state['df'] = None
        if 'X_train' not in st.session_state:
            st.session_state['X_train'] = None
        if 'X_test' not in st.session_state:
            st.session_state['X_test'] = None
        if 'y_train' not in st.session_state:
            st.session_state['y_train'] = None
        if 'y_test' not in st.session_state:
            st.session_state['y_test'] = None
        if 'X_val' not in st.session_state:
            st.session_state['X_val'] = None
        if 'y_val' not in st.session_state:
            st.session_state['y_val'] = None
        if "model" not in st.session_state:
            st.session_state['model'] = None
        if 'trained_model' not in st.session_state:
            st.session_state['trained_model'] = False
        if "trained_model_bool" not in st.session_state:
            st.session_state['trained_model_bool'] = False
        if "problem_type" not in st.session_state:
            st.session_state['problem_type'] = None
        if "metrics_df" not in st.session_state:
            st.session_state['metrics_df'] = pd.DataFrame()
        if "is_train" not in st.session_state:
            st.session_state['is_train'] = False
        if "is_test" not in st.session_state:
            st.session_state['is_test'] = False
        if "is_val" not in st.session_state:
            st.session_state['is_val'] = False
        if "show_eval" not in st.session_state:
            st.session_state['show_eval'] = False
        if "all_the_process" not in st.session_state:
            st.session_state['all_the_process'] = ""
        if "all_the_process_predictions" not in st.session_state:
            st.session_state['all_the_process_predictions'] = False
        if 'y_pred_train' not in st.session_state:
            st.session_state['y_pred_train'] = None
        if 'y_pred_test' not in st.session_state:
            st.session_state['y_pred_test'] = None
        if 'y_pred_val' not in st.session_state:
            st.session_state['y_pred_val'] = None
        if 'uploading_way' not in st.session_state:
            st.session_state['uploading_way'] = None
        if "lst_models" not in st.session_state:
            st.session_state["lst_models"] = []
        if "lst_models_predctions" not in st.session_state:
            st.session_state["lst_models_predctions"] = []
        if "models_with_eval" not in st.session_state:
            st.session_state["models_with_eval"] = dict()
        if "reset_1" not in st.session_state:
            st.session_state["reset_1"] = False

    initial_state()

    def new_line(n=1):
        for _ in range(n):
            st.write("\n")
    
    # Keep the space buffer clean
    new_line(1)

    # Core Academic & Project Branding Description
    st.markdown(
        """
        <h1 align='center' style='color: #1E88E5;'>🦾 The Pro Coach</h1>
        <h3 align='center'>AI Vision-Based Solo Training Assistant</h3>
        <p style='text-align: justify;'>
        Welcome to <b>The Pro Coach</b>, a high-performance biomechanical assessment platform designed for unconstrained training environments. 
        Leveraging MediaPipe BlazePose landmark extraction pipelines alongside continuous angular heuristic analysis, this application eliminates the 
        traditional supervision gap in home fitness and athletics by providing clinical-grade real-time posture valuation.
        </p>
        """,
        unsafe_allow_html=True
    )
    st.divider()

    st.markdown("<h2 align='center'>🏆 Your Fitness Dashboard</h2>", unsafe_allow_html=True)
    new_line(1)

    # Gamification stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='premium-card'><p>Current Level</p><h2>5</h2><p class='sub-text'>Iron Lifter</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='premium-card'><p>Total XP</p><h2>12.4k</h2><p class='sub-text'>Top 15% of users</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='premium-card'><p>Active Streak</p><h2>4</h2><p class='sub-text'>Days 🔥</p></div>", unsafe_allow_html=True)
    
    new_line(2)
    st.progress(75, text="75% to Level 6 (Titan)")

    new_line(2)
    st.markdown("<h2 align='center'>🚀 Getting Started</h2>", unsafe_allow_html=True)
    st.info(
        "To begin monitoring your kinematics, select an active workspace module from the sidebar. "
        "Choose between **Live Stream** via your webcam or **Upload an existing video**."
    )