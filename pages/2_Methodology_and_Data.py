import os
import sys

import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()

from thresholds import get_thresholds_beginner as get_squat_beginner, get_thresholds_pro as get_squat_pro
from threshold_pushups import get_thresholds_beginner as get_pushup_beginner
from threshold_curl import get_thresholds_beginner as get_curl_beginner
from threshold_kickback import get_thresholds_beginner as get_kickback_beginner

st.title("Methodology and Data")

st.markdown("### Model")
st.markdown(
    "- Approach: this project uses a pretrained pose-estimation model (transfer of an existing model) instead of training a new one. Pose landmarks come from the pretrained MediaPipe Pose (BlazePose) model that is bundled inside the mediapipe package (version pinned in requirements.txt). BlazePose is designed for real-time, CPU-only inference.\n"
    "- Training data: the BlazePose weights were trained by their authors (Google) on their own data. That data is not part of this repository and was not used or modified here. No model was trained or fine-tuned in this project, and this repository contains no training dataset.\n"
    "- Our contribution: converting landmarks to joint and segment-to-vertical angles, exercise-specific finite state machines for repetition counting, rule-based form checks, voice and visual feedback, and the Streamlit web application.\n"
    "- Rule-based logic: thresholds are hand-set and defined in thresholds.py, threshold_pushups.py, threshold_curl.py, threshold_kickback.py and threshold_lunges.py, and in the page scripts of the additional exercises. They are not learned from data.\n"
    "- OpenPose is not used.\n"
    "- Evaluation data: our own recorded exercise videos and manual labels are not part of this repository. See evaluation/README.md for the protocol and how accuracy is computed from evaluation/trials.csv.\n"
    "- output_sample.mp4 is a bicep-curl demonstration video used on the Demo page.\n"
)

st.markdown("### Training data")
st.markdown(
    "- The BlazePose weights were trained by their authors (Google) on their own data. That data is not part of this repository and was not used or modified here. No model was trained or fine-tuned in this project, and this repository contains no training dataset."
)

st.markdown("### What this project adds")
st.markdown(
    "- Converting landmarks to joint and segment-to-vertical angles, exercise-specific finite state machines for repetition counting, rule-based form checks, voice and visual feedback, and the Streamlit web application.\n"
    "- View-size controls, voice feedback that repeats on-screen messages, and rule-based post-workout suggestions.\n"
    "- Beginner guides, voice feedback, post-workout suggestions and session history."
)

st.markdown("### Thresholds")
with st.expander("Squat thresholds"):
    st.json({
        "squat_beginner": get_squat_beginner(),
        "squat_pro": get_squat_pro(),
    })
with st.expander("Push-up thresholds"):
    st.json(get_pushup_beginner())
with st.expander("Curl thresholds"):
    st.json(get_curl_beginner())
with st.expander("Kickback thresholds"):
    st.json(get_kickback_beginner())

st.markdown("Webcam frame -> pretrained MediaPipe Pose (33 landmarks) -> joint/vertical angles -> exercise FSM -> overlay + voice feedback")

st.markdown("### Evaluation data")
st.markdown(
    "- Our own recorded exercise videos and manual labels are not part of this repository. See evaluation/README.md for the protocol and how accuracy is computed from evaluation/trials.csv."
)

if os.path.exists("evaluation/trials.csv"):
    from evaluate_trials import compute_accuracy

    st.markdown("## Evaluation results")
    results = compute_accuracy("evaluation/trials.csv")
    if "message" in results:
        st.info(results["message"])
    else:
        st.dataframe(pd.DataFrame(results.get("exercise_results", [])))
else:
    st.markdown("## Evaluation results")
    st.info("No evaluation file found. Add evaluation/trials.csv to display accuracy results.")
