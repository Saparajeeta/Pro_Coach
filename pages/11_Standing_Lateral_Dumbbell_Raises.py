import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import av
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes

st.set_page_config(page_title="Lateral Raises AI", page_icon="🏋️", layout="wide")
st.title("🏋️ Standing Lateral Dumbbell Raises AI")
st.markdown("Track your lateral raises. Do not raise your arms past 100 degrees (abduction angle).")

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

class LateralRaisesProcessor:
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
            # 23-11-13 and 24-12-14
            l_hip = [landmarks[23].x, landmarks[23].y]
            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_elbow = [landmarks[13].x, landmarks[13].y]
            
            r_hip = [landmarks[24].x, landmarks[24].y]
            r_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[14].x, landmarks[14].y]
            
            l_angle = calculate_angle(l_hip, l_shoulder, l_elbow)
            r_angle = calculate_angle(r_hip, r_shoulder, r_elbow)
            
            avg_angle = (l_angle + r_angle) / 2.0
            
            color = (0, 255, 0)
            warning_text = ""
            
            if avg_angle > 100:
                color = (0, 0, 255) # Red for form error
                warning_text = "WARNING: Arms too high!"
                
            # FSM Logic
            # State 1: Down (< 30)
            # State 2: Transition (30 to 75)
            # State 3: Peak (75 to 100)
            if avg_angle < 30:
                if self.state == 3:
                    self.counter += 1
                self.state = 1
            elif 30 <= avg_angle < 75:
                self.state = 2
            elif 75 <= avg_angle <= 100:
                self.state = 3

            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2)
            )

            cv2.rectangle(image, (0, 0), (450, 120), (0, 0, 0), -1)
            cv2.putText(image, f'REPS: {self.counter}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'ANGLE: {int(avg_angle)}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            if warning_text:
                cv2.putText(image, warning_text, (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass

        return image

processor = LateralRaisesProcessor()

def video_frame_callback(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    img = processor.process(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="lateral-raises",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False)
)
