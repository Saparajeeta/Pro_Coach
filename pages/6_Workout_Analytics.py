import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="Workout Analytics", page_icon="📊", layout="wide")

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import custom_style
custom_style.apply_custom_style()

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()


st.markdown(
    """
    <style>
    .pb-card {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        border: 1px solid #1E88E5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .pb-card h3 { color: #1E88E5; margin: 0; font-size: 1.5rem; }
    .pb-card p { color: #FFF; margin: 0; font-size: 2rem; font-weight: bold; }
    .pb-card span { font-size: 0.9rem; color: #AAA; }
    </style>
    """, unsafe_allow_html=True
)

st.title("📊 Workout Analytics Dashboard")
st.markdown("Analyze your kinematic telemetry, review accuracy trends, and track your PRs.")

@st.cache_data
def get_mock_data():
    dates = [datetime.now() - timedelta(days=i) for i in range(14, -1, -1)]
    data = {
        'Date': dates,
        'Exercise': ['Bicep Curls', 'Squats', 'Lunges', 'Push-ups', 'Bicep Curls', 'Rest', 'Squats', 'Push-ups', 'Lunges', 'Bicep Curls', 'Rest', 'Squats', 'Push-ups', 'Lunges', 'Bicep Curls'],
        'Correct Reps': [15, 20, 12, 10, 18, 0, 22, 15, 14, 20, 0, 25, 20, 16, 22],
        'Incorrect Reps': [3, 5, 2, 4, 2, 0, 4, 3, 3, 1, 0, 3, 2, 2, 1],
        'Calories Burned': [120, 200, 150, 100, 140, 0, 220, 150, 170, 160, 0, 250, 200, 180, 170]
    }
    df = pd.DataFrame(data)
    df_active = df[df['Exercise'] != 'Rest'].copy()
    df_active['Accuracy (%)'] = (df_active['Correct Reps'] / (df_active['Correct Reps'] + df_active['Incorrect Reps']) * 100).round(1)
    df_active['Workout Score'] = (df_active['Correct Reps'] * 10 + df_active['Accuracy (%)'] * 2).round(0)
    return df, df_active

df_all, df = get_mock_data()

st.markdown("### 🏆 Personal Bests")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown("<div class='pb-card'><h3>Squats</h3><p>25</p><span>Max Reps / Session</span></div>", unsafe_allow_html=True)
with c2:
    st.markdown("<div class='pb-card'><h3>Push-ups</h3><p>20</p><span>Max Reps / Session</span></div>", unsafe_allow_html=True)
with c3:
    st.markdown("<div class='pb-card'><h3>Bicep Curls</h3><p>22</p><span>Max Reps / Session</span></div>", unsafe_allow_html=True)
with c4:
    st.markdown("<div class='pb-card'><h3>Best Accuracy</h3><p>95.7%</p><span>Overall Session</span></div>", unsafe_allow_html=True)

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Muscle Group Balance")
    categories = ['Chest', 'Legs', 'Arms', 'Core', 'Back']
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[20, 45, 30, 10, 15],
        theta=categories,
        fill='toself',
        name='Weekly Volume',
        marker=dict(color='#1E88E5')
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("Reps Volume Over Time")
    fig_volume = px.bar(df, x='Date', y=['Correct Reps', 'Incorrect Reps'], 
                        title="Form Validation (Correct vs Incorrect)",
                        barmode='group',
                        color_discrete_sequence=['#1E88E5', '#FF4B4B'])
    fig_volume.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
    st.plotly_chart(fig_volume, use_container_width=True)

st.divider()
st.subheader("Kinematic Accuracy Trend")
fig_acc = px.line(df, x='Date', y='Accuracy (%)', color='Exercise', markers=True, 
                  title="Form Accuracy Tracking by Exercise",
                  color_discrete_sequence=px.colors.qualitative.Pastel)
fig_acc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="white"))
st.plotly_chart(fig_acc, use_container_width=True)

import json
import os

st.divider()
st.markdown("## 🧠 Generative Biomechanical Planner")
st.markdown("Your custom corrective routines based on real-time kinematic form breaks detected during your session.")

log_file = "session_mistakes.json"
mistakes_found = set()

if os.path.exists(log_file):
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
            for m in logs:
                mistakes_found.add(m.get("mistake"))
    except:
        pass

if not mistakes_found:
    st.success("No critical form breaks detected recently! Keep up the great work.")
else:
    for mistake in mistakes_found:
        if mistake == "Asymmetrical Squat Load":
            with st.expander("⚠️ Asymmetrical Squat Load Detected", expanded=True):
                st.write("**Biomechanics Engine Log:** The system detected a dangerous lateral weight shift during your squat descent. One knee/hip is dropping faster than the other, placing uneven load on your joints.")
                st.markdown("### Corrective Plan Generated:")
                st.info("- **Single-Leg Bulgarian Split Squats:** 3 sets of 10 per leg. (Forces independent leg stabilization)\n- **Hip Abductor Raises:** 3 sets of 15 per leg. (Strengthens gluteus medius to prevent lateral hip shift)\n- **Tempo Squats (3-1-1):** 3 sets of 8. (Focus on perfectly symmetrical descent)")
        elif mistake == "Sagging Back in Pushups":
            with st.expander("⚠️ Sagging Back in Push-ups Detected", expanded=True):
                st.write("**Biomechanics Engine Log:** The system detected that your hip angle broke below the safety threshold, indicating weak core engagement during pressing.")
                st.markdown("### Corrective Plan Generated:")
                st.info("- **Hollow Body Holds:** 4 sets of 30 seconds. (Trains anti-extension of the spine)\n- **Planks with Shoulder Taps:** 3 sets of 20 taps. (Builds dynamic core stability)\n- **Incline Push-ups:** 3 sets of 15. (Allows you to focus on rigid core alignment with less resistance)")
        else:
            with st.expander(f"⚠️ {mistake}", expanded=True):
                st.write("**Biomechanics Engine Log:** This form break was logged by the AI.")
                st.markdown("### Corrective Plan Generated:")
                st.info("Focus on lighter weights and form-specific isolation exercises.")
