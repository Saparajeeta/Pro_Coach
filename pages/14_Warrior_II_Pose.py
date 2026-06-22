import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes
from aiortc.contrib.media import MediaRecorder
import os

st.set_page_config(page_title="Warrior II AI", page_icon="🧘", layout="wide")
st.title("🧘 Warrior II Pose (Virabhadrasana II)")
st.markdown("Hold your Warrior II pose. Keep your front knee bent and arms raised.")

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

class WarriorIIProcessor:
    def __init__(self):
        self.start_time = None
        self.pose_held = False
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
            # Knees
            l_hip = [landmarks[23].x, landmarks[23].y]
            l_knee = [landmarks[25].x, landmarks[25].y]
            l_ankle = [landmarks[27].x, landmarks[27].y]
            
            r_hip = [landmarks[24].x, landmarks[24].y]
            r_knee = [landmarks[26].x, landmarks[26].y]
            r_ankle = [landmarks[28].x, landmarks[28].y]
            
            l_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
            r_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
            
            front_knee_angle = min(l_knee_angle, r_knee_angle)
            
            # Arms (13-11-23 and 14-12-24)
            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_elbow = [landmarks[13].x, landmarks[13].y]
            
            r_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[14].x, landmarks[14].y]
            
            l_arm_angle = calculate_angle(l_elbow, l_shoulder, l_hip)
            r_arm_angle = calculate_angle(r_elbow, r_shoulder, r_hip)
            
            color = (0, 255, 0)
            warning_text = ""
            
            # Target Criteria: front knee <= 110, both shoulders near 90 (let's say 75 to 105)
            arms_correct = (75 <= l_arm_angle <= 105) and (75 <= r_arm_angle <= 105)
            knee_correct = front_knee_angle <= 110
            
            if arms_correct and knee_correct:
                if not self.pose_held:
                    self.start_time = time.time()
                    self.pose_held = True
            else:
                self.pose_held = False
                self.start_time = None
                color = (0, 0, 255)
                if not arms_correct:
                    warning_text = "Keep your arms parallel to the ground!"
                elif not knee_correct:
                    warning_text = "Bend your front knee more!"

            hold_duration = 0
            if self.pose_held and self.start_time is not None:
                hold_duration = int(time.time() - self.start_time)

            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2)
            )

            cv2.rectangle(image, (0, 0), (600, 120), (0, 0, 0), -1)
            if self.pose_held:
                cv2.putText(image, f'HOLD TIME: {hold_duration} s', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            else:
                cv2.putText(image, 'GET INTO POSE', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            
            if warning_text:
                cv2.putText(image, warning_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass

        return image

processor = WarriorIIProcessor()

if 'download_warrior' not in st.session_state:
    st.session_state['download_warrior'] = False

output_video_file = 'output_warrior.flv'

def out_recorder_factory() -> MediaRecorder:
    return MediaRecorder(output_video_file)

def video_frame_callback(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    img = processor.process(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="warrior-ii",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
    out_recorder_factory=out_recorder_factory
)

download_button = st.empty()

if os.path.exists(output_video_file):
    with open(output_video_file, 'rb') as op_vid:
        download = download_button.download_button('Download Video', data=op_vid, file_name='warrior_ii_live.flv')
        if download:
            st.session_state['download_warrior'] = True

if os.path.exists(output_video_file) and st.session_state['download_warrior']:
    os.remove(output_video_file)
    st.session_state['download_warrior'] = False
    download_button.empty()
