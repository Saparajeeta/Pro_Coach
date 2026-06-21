import streamlit as st
from pathlib import Path
from Homepage import set_sidebar_visibility

set_sidebar_visibility(st.session_state.get("authentication_status"))

st.set_page_config(layout="wide", page_title="Form Masterclass")

st.markdown(
    """
    <style>
    .masterclass-header {
        font-size: 3rem;
        font-weight: 900;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    </style>
    <div class="masterclass-header">🏋️‍♂️ Form Masterclass</div>
    <div class="sub-header">Interactive Demo: AI Squats Analysis</div>
    """, unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    base_dir = Path(__file__).resolve().parent.parent
    video_path = base_dir / "output_sample.mp4"

    if video_path.exists():
        st.video(str(video_path))
    else:
        st.warning("Sample video not found.")
        st.info(f"Expected file location: {video_path}")
        st.write("Place 'output_sample.mp4' in the project root folder to display the demo video.")

with col2:
    st.markdown("### 🔬 Biomechanics Breakdown")
    st.info("The AI continuously tracks key angular heuristics to ensure clinical-grade form.")
    
    with st.expander("1️⃣ Knee-Hip Alignment", expanded=True):
        st.write("Ensures your knees do not track too far past your toes. The AI calculates the horizontal offset between your knee joint and foot coordinates.")
        st.progress(100, text="Tracking Accuracy: 98%")
        
    with st.expander("2️⃣ Spinal Posture (Back Angle)", expanded=True):
        st.write("Detects if your back is rounding or overextending by calculating the shoulder-hip-knee angle.")
        st.progress(95, text="Tracking Accuracy: 95%")
        
    with st.expander("3️⃣ Squat Depth", expanded=True):
        st.write("Measures the angle between your hip, knee, and ankle. A 'pass' is triggered when the hip crease goes below the top of the knee.")
        st.progress(99, text="Tracking Accuracy: 99%")

st.divider()
st.markdown("<h4 align='center'>Ready to test your own form?</h4>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
with col_btn2:
    st.page_link("pages/Squat AI Trainer.py", label="🚀 Launch Squat AI Trainer", use_container_width=True)