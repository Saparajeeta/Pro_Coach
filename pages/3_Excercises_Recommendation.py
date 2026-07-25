import streamlit as st
import datetime
import json
from Homepage import set_sidebar_visibility

set_sidebar_visibility(st.session_state.get("authentication_status"))

st.set_page_config(layout="wide", page_title="AI Exercise Plan")

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import custom_style
custom_style.apply_custom_style()

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()


st.markdown(
    """
    <style>
    .wizard-header { font-size: 2.5rem; font-weight: bold; color: #1E88E5; margin-bottom: 0px; }
    .wizard-sub { color: #888; font-size: 1.1rem; margin-bottom: 20px; }
    .bmi-card { padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 1.5rem; }
    </style>
    <div class="wizard-header">✨ AI Workout Plan Generator</div>
    <div class="wizard-sub">Answer a few questions to get your personalized, calendar-synced routine.</div>
    """, unsafe_allow_html=True
)

today = datetime.date.today()

col_input, col_bmi = st.columns([2, 1])

with col_input:
    st.markdown("### 📋 Your Profile")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            user_height = st.text_input("Height (cm):", "175", key="height")
            push_up = st.slider("Max Push-ups in a row?", 0, 100, 15, key="push_up")
            goal = st.selectbox("Fitness Goal:", ["Lose weight", "Bulk up", "Cut"], key="goal")
        with c2:
            user_weight = st.text_input("Weight (kg):", "70", key="weight")
            user_days = st.slider("Days per week?", 1, 7, 4, key="days")
            experience = st.selectbox("Experience Level:", ["Beginner", "Intermediate", "Advanced"], key="experience")

with col_bmi:
    st.markdown("### 📊 Health Metrics")
    try:
        h_m = float(user_height) / 100
        w_kg = float(user_weight)
        bmi = w_kg / (h_m * h_m)
        
        if bmi < 18.5:
            color, status = "#FFB3BA", "Underweight"
        elif 18.5 <= bmi < 25:
            color, status = "#BAFFC9", "Healthy"
        elif 25 <= bmi < 30:
            color, status = "#FFFFBA", "Overweight"
        else:
            color, status = "#FFC8C8", "Obese"
            
        st.markdown(f"<div class='bmi-card' style='background-color: {color}; color: black;'>BMI: {bmi:.1f}<br><span style='font-size: 1rem;'>{status}</span></div>", unsafe_allow_html=True)
    except:
        st.info("Enter valid height and weight to calculate BMI.")

st.divider()

def generate_plan(days, goal, experience, pushups):
    days = max(1, min(days, 7))

    beginner_plan = [
        ("Upper Body", ["Push-ups - 3 x 8 x Bodyweight", "Dumbbell Press - 3 x 10 x Light", "Bicep Curl - 3 x 12 x Light"]),
        ("Lower Body", ["Squats - 3 x 12 x Bodyweight", "Lunges - 3 x 10 x Bodyweight", "Glute Bridge - 3 x 15 x Bodyweight"]),
        ("Cardio + Core", ["Brisk Walk - 20 min", "Plank - 3 x 30 sec", "Mountain Climbers - 3 x 20"]),
        ("Full Body", ["Deadlift - 3 x 8 x Light", "Shoulder Press - 3 x 10 x Light", "Step-ups - 3 x 10 each leg"]),
        ("Active Recovery", ["Stretching - 20 min", "Yoga - 20 min", "Mobility Drills - 15 min"]),
        ("Leg Focus", ["Goblet Squat - 3 x 10 x Light", "Romanian Deadlift - 3 x 10 x Light", "Calf Raises - 3 x 20"]),
        ("Rest / Recovery", ["Walking - 20 min", "Foam Rolling - 10 min"]),
    ]

    intermediate_plan = [
        ("Push Day", ["Bench Press - 4 x 8 x Moderate", "Shoulder Press - 4 x 10 x Moderate", "Tricep Dips - 3 x 12"]),
        ("Pull Day", ["Lat Pulldown - 4 x 10 x Moderate", "Seated Row - 4 x 10 x Moderate", "Bicep Curl - 3 x 12 x Moderate"]),
        ("Leg Day", ["Back Squat - 4 x 8 x Moderate", "Romanian Deadlift - 4 x 10 x Moderate", "Walking Lunges - 3 x 12"]),
        ("Core + Cardio", ["Plank - 3 x 45 sec", "Hanging Knee Raises - 3 x 12", "Jogging - 25 min"]),
        ("Upper Body", ["Incline Press - 4 x 8", "Lateral Raises - 3 x 15", "Push-ups - 3 x max"]),
        ("Lower Body", ["Front Squat - 4 x 8", "Leg Press - 3 x 12", "Hamstring Curl - 3 x 12"]),
        ("Rest / Recovery", ["Stretching - 20 min", "Mobility - 15 min"]),
    ]

    advanced_plan = [
        ("Push Strength", ["Bench Press - 5 x 5 x Heavy", "Overhead Press - 4 x 6 x Heavy", "Weighted Dips - 4 x 8"]),
        ("Pull Strength", ["Weighted Pull-up - 5 x 5", "Barbell Row - 4 x 8 x Heavy", "Hammer Curl - 4 x 10"]),
        ("Leg Strength", ["Back Squat - 5 x 5 x Heavy", "Deadlift - 4 x 5 x Heavy", "Bulgarian Split Squat - 4 x 8"]),
        ("Conditioning", ["Rowing - 20 min", "Burpees - 4 x 15", "Battle Rope - 5 x 30 sec"]),
        ("Hypertrophy Upper", ["Incline Dumbbell Press - 4 x 12", "Cable Fly - 3 x 15", "Arnold Press - 3 x 12"]),
        ("Hypertrophy Lower", ["Front Squat - 4 x 10", "Leg Extension - 3 x 15", "RDL - 4 x 10"]),
        ("Recovery", ["Mobility - 20 min", "Light Cardio - 20 min"]),
    ]

    if experience == "Beginner":
        base_plan = beginner_plan
    elif experience == "Intermediate":
        base_plan = intermediate_plan
    else:
        base_plan = advanced_plan

    if goal == "Lose weight":
        color = "#FFB3BA"
    elif goal == "Bulk up":
        color = "#BAFFC9"
    else:
        color = "#BAE1FF"

    selected_days = base_plan[:days]
    events = []
    
    plan_data = []

    for i, (focus, exercises) in enumerate(selected_days):
        workout_date = today + datetime.timedelta(days=i)
        
        day_str = f"Day {i+1}: {focus}"
        plan_data.append({"Day": day_str, "Date": workout_date.strftime("%a, %b %d"), "Exercises": " • ".join(exercises)})
        
        for exercise in exercises:
            events.append({
                "title": exercise,
                "color": color,
                "start": str(workout_date),
                "end": str(workout_date),
                "resourceId": ["a", "b", "c", "d", "e", "f"][i % 6],
            })

    return plan_data, events

btn_col1, btn_col2, btn_col3 = st.columns([1,2,1])
with btn_col2:
    submit = st.button("🚀 Generate Personalized Plan", use_container_width=True, type="primary")

if submit:
    with st.spinner("Analyzing profile and building optimal routine..."):
        plan_data, events = generate_plan(user_days, goal, experience, push_up)
        
        st.markdown("### 🏆 Your Custom Weekly Plan")
        
        for p in plan_data:
            with st.expander(f"📅 {p['Date']} - **{p['Day']}**", expanded=True):
                st.write(p['Exercises'])

        st.session_state["transferred_variable"] = json.dumps(events)
        st.session_state["events"] = events

        st.success("✅ Workout plan generated and synced to the Calendar page!")
