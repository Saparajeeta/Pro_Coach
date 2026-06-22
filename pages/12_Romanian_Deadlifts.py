import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import av
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
from aiortc.contrib.media import MediaRecorder
import os

st.set_page_config(page_title="RDL AI Trainer", page_icon="🏋️", layout="wide")
st.title("🏋️ Romanian Deadlifts AI Trainer")
st.markdown("Track your hip hinge and knee bend. Ensure your legs stay mostly straight.")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    if np.linalg.norm(ba) == 0 or np.linalg.norm(bc) == 0:
        return 0.0
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

class RDLProcessor:
    def __init__(self):
        self.state = 1
        self.counter = 0
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.pose.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if not results.pose_landmarks:
            return image

        landmarks = results.pose_landmarks.landmark
        
        try:
            # We use the left side (11-23-25 for hip hinge, 23-25-27 for knee)
            # Assuming left side is facing camera. In production we might check visibility.
            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_hip = [landmarks[23].x, landmarks[23].y]
            l_knee = [landmarks[25].x, landmarks[25].y]
            l_ankle = [landmarks[27].x, landmarks[27].y]
            
            hip_angle = calculate_angle(l_shoulder, l_hip, l_knee)
            knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
            
            color = (0, 255, 0)
            warning_text = ""
            
            # Form check: knee drops below 150 -> warning
            if knee_angle < 150:
                color = (0, 0, 255) # Red
                warning_text = "Keep legs straight, hinge at hips!"
                
            # FSM Logic for RDL
            # State 1: Upright (Hip > 160)
            # State 2: Hinging (120 < Hip <= 160)
            # State 3: Peak Hinge (Hip <= 120)
            if hip_angle > 160:
                if self.state == 3:
                    self.counter += 1
                self.state = 1
            elif 120 < hip_angle <= 160:
                self.state = 2
            elif hip_angle <= 120:
                self.state = 3

            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2)
            )

            cv2.rectangle(image, (0, 0), (600, 120), (0, 0, 0), -1)
            cv2.putText(image, f'REPS: {self.counter}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'HIP: {int(hip_angle)} | KNEE: {int(knee_angle)}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            if warning_text:
                cv2.putText(image, warning_text, (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass

        return image

processor = RDLProcessor()

if 'download_rdl' not in st.session_state:
    st.session_state['download_rdl'] = False

output_video_file = 'output_rdl.flv'

def out_recorder_factory() -> MediaRecorder:
    return MediaRecorder(output_video_file)

def video_frame_callback(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    img = processor.process(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="rdl",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
    out_recorder_factory=out_recorder_factory
)

download_button = st.empty()

if os.path.exists(output_video_file):
    with open(output_video_file, 'rb') as op_vid:
        download = download_button.download_button('Download Video', data=op_vid, file_name='rdl_live.flv')
        if download:
            st.session_state['download_rdl'] = True

if os.path.exists(output_video_file) and st.session_state['download_rdl']:
    os.remove(output_video_file)
    st.session_state['download_rdl'] = False
    download_button.empty()
