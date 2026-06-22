import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoHTMLAttributes

st.set_page_config(page_title="Tree Pose AI", page_icon="🧘", layout="wide")
st.title("🧘 Tree Pose (Vrikshasana)")
st.markdown("Hold your tree pose. The timer starts when your knee angle is <= 60 degrees.")

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

class TreePoseProcessor:
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
            l_hip = [landmarks[23].x, landmarks[23].y]
            l_knee = [landmarks[25].x, landmarks[25].y]
            l_ankle = [landmarks[27].x, landmarks[27].y]
            
            r_hip = [landmarks[24].x, landmarks[24].y]
            r_knee = [landmarks[26].x, landmarks[26].y]
            r_ankle = [landmarks[28].x, landmarks[28].y]
            
            l_knee_angle = calculate_angle(l_hip, l_knee, l_ankle)
            r_knee_angle = calculate_angle(r_hip, r_knee, r_ankle)
            
            # Find the lifted knee
            lifted_knee_angle = min(l_knee_angle, r_knee_angle)
            
            # Hip stability (angle between 23-24 line and horizontal)
            dx = r_hip[0] - l_hip[0]
            dy = r_hip[1] - l_hip[1]
            hip_tilt = np.degrees(np.arctan2(abs(dy), abs(dx)))
            
            color = (0, 255, 0)
            warning_text = ""
            
            if hip_tilt > 10:
                color = (0, 0, 255)
                warning_text = "Keep your hips level!"
                self.pose_held = False
                self.start_time = None
            elif lifted_knee_angle <= 60:
                if not self.pose_held:
                    self.start_time = time.time()
                    self.pose_held = True
            else:
                self.pose_held = False
                self.start_time = None
                color = (0, 0, 255)
                
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

            cv2.rectangle(image, (0, 0), (450, 120), (0, 0, 0), -1)
            if self.pose_held:
                cv2.putText(image, f'HOLD TIME: {hold_duration} s', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            else:
                cv2.putText(image, 'GET INTO POSE', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
            
            if warning_text:
                cv2.putText(image, warning_text, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
            
        except Exception as e:
            pass

        return image

processor = TreePoseProcessor()

def video_frame_callback(frame: av.VideoFrame):
    img = frame.to_ndarray(format="bgr24")
    img = processor.process(img)
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(
    key="tree-pose",
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": True, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False)
)
