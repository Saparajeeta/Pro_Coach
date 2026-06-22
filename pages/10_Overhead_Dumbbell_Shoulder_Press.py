import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import av
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes

# Streamlit UI configuration
st.set_page_config(page_title="Shoulder Press AI", page_icon="🏋️", layout="wide")
st.title("🏋️ Overhead Dumbbell Shoulder Press AI Trainer")
st.markdown("Track your Overhead Dumbbell Shoulder Press form in real-time. Ensure your elbows drop to 90 degrees and fully extend at the top.")

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

class ShoulderPressProcessor:
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
            # Get coordinates
            l_shoulder = [landmarks[11].x, landmarks[11].y]
            l_elbow = [landmarks[13].x, landmarks[13].y]
            l_wrist = [landmarks[15].x, landmarks[15].y]
            
            r_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[14].x, landmarks[14].y]
            r_wrist = [landmarks[16].x, landmarks[16].y]
            
            # Calculate angles
            l_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
            r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            
            avg_angle = (l_angle + r_angle) / 2.0
            
            # FSM Logic
            # State 1: Extension Base (Down, angle <= 100)
            # State 2: Transition Phase (100 < angle < 160)
            # State 3: Peak Contraction (Up, angle >= 160)
            
            color = (0, 255, 0) # Green for good form
            
            if avg_angle <= 100:
                if self.state == 3:
                    self.counter += 1
                self.state = 1
            elif 100 < avg_angle < 160:
                self.state = 2
            elif avg_angle >= 160:
                self.state = 3

            # Draw Skeletal Lines
            mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=color, thickness=2, circle_radius=2)
            )

            # Dashboard UI
            cv2.rectangle(image, (0, 0), (350, 120), (0, 0, 0), -1)
            cv2.putText(image, f'REPS: {self.counter}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'STATE: {self.state}', (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(image, f'ANGLE: {int(avg_angle)}', (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass

        return image

processor = ShoulderPressProcessor()

def video_frame_callback(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    img = processor.process(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="shoulder-press",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False)
)
