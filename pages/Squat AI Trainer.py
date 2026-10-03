import av
import os
import sys
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from exercise_guides import render_guide
from view_options import render_view_controls
import session_stats
from workout_summary import start_workout, render_finish_workout
import custom_style
custom_style.apply_custom_style()

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)
import av
import os
import sys
import streamlit as st
from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
from aiortc.contrib.media import MediaRecorder


BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)


from utils import get_mediapipe_pose
from process_frame_squats import ProcessFrame
from thresholds import get_thresholds_beginner

st.title('Squat AI Trainer')
render_guide("Squats")
session_started_at = start_workout("Squats")


thresholds = None 


thresholds = get_thresholds_beginner()



live_process_frame = ProcessFrame(thresholds=thresholds, flip_frame=True)
# Initialize face mesh solution
pose = get_mediapipe_pose()


if 'download' not in st.session_state:
    st.session_state['download'] = False

output_video_file = f'output_live.flv'

  

def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format="rgb24")  # Decode and get RGB frame
    frame, _ = live_process_frame.process(frame, pose)  # Process frame
    session_stats.update("Squats", live_process_frame.state_tracker["SQUAT_COUNT"], live_process_frame.state_tracker["IMPROPER_SQUAT"])
    import cv2
    frame = cv2.resize(frame, (720, 480))
    return av.VideoFrame.from_ndarray(frame, format="rgb24")  # Encode and return BGR frame


def out_recorder_factory() -> MediaRecorder:
        return MediaRecorder(output_video_file)


stream_column = render_view_controls("squats")
st.caption("Before you start: stand so your whole body is visible, with the side or front view shown in the guide, and good lighting.")

with stream_column:
    ctx = webrtc_streamer(
                            key="Squats-pose-analysis",
                            video_frame_callback=video_frame_callback,
                            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},  # Add this config
                            media_stream_constraints={"video": {"width": {'min':1080, 'ideal':2160}}, "audio": False},
                            video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
                            out_recorder_factory=out_recorder_factory
                        )

    download_button = st.empty()

    if os.path.exists(output_video_file):
        with open(output_video_file, 'rb') as op_vid:
            download = download_button.download_button('Download Video', data = op_vid, file_name='output_live.flv')

            if download:
                st.session_state['download'] = True

    if os.path.exists(output_video_file) and st.session_state['download']:
        os.remove(output_video_file)
        st.session_state['download'] = False
        download_button.empty()

render_finish_workout("Squats", session_started_at)


    




from utils import get_mediapipe_pose
from process_frame_squats import ProcessFrame
from thresholds import get_thresholds_beginner, get_thresholds_pro

st.title('AI Squats correction')
