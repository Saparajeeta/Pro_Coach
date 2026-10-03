import os
import sys

import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core import custom_style
from core.dependency_utils import load_webrtc_dependencies, project_path

av, VideoHTMLAttributes, webrtc_streamer, MediaRecorder = load_webrtc_dependencies(
    "the Football Kick webcam module"
)

custom_style.apply_custom_style()

if not st.session_state.get('authentication_status'):
    st.info('Please login from the Homepage to access this module.')
    st.stop()

BASE_DIR = os.path.abspath(os.path.join(__file__, '../../'))
sys.path.append(BASE_DIR)

from core.utils import get_mediapipe_pose
from exercise_guides import render_guide
from core.process_frame_football import ProcessFrameFootball
from core.threshold_football import get_thresholds_beginner
from core.db_utils import record_processor_session

st.title('Football Kick Mechanics Lab')
render_guide("Football Kick")
st.session_state['active_exercise'] = 'Football Kick'
st.caption('Analyze backswing loading, knee snap speed, and plant-foot spacing from a side-on camera angle.')
st.info(
    'Use a full-body, side-on setup and leave enough space to swing through naturally. '
    'The tracker compares the active kicking leg against the plant leg in real time.'
)

thresholds = get_thresholds_beginner()
live_process_frame = ProcessFrameFootball(thresholds=thresholds, flip_frame=True)
pose = get_mediapipe_pose()

if 'football_download' not in st.session_state:
    st.session_state['football_download'] = False

output_video_file = project_path('output_live_football.flv')


def video_frame_callback(frame: av.VideoFrame):
    frame = frame.to_ndarray(format='rgb24')
    frame, _ = live_process_frame.process(frame, pose)
    import cv2

    frame = cv2.resize(frame, (720, 480))
    return av.VideoFrame.from_ndarray(frame, format='rgb24')


def out_recorder_factory() -> MediaRecorder:
    return MediaRecorder(output_video_file)


ctx = webrtc_streamer(
    key='Football-kick-analysis',
    video_frame_callback=video_frame_callback,
    rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    media_stream_constraints={"video": {"width": {'min': 1080, 'ideal': 2160}}, "audio": False},
    video_html_attrs=VideoHTMLAttributes(autoPlay=True, controls=False, muted=False),
    out_recorder_factory=out_recorder_factory,
)

if getattr(ctx.state, 'playing', False):
    st.session_state['football_session_active'] = True
elif st.session_state.pop('football_session_active', False):
    record_processor_session(live_process_frame, 'Football Kick', st.session_state.get('username', 'anonymous'), 'football')

download_button = st.empty()

if os.path.exists(output_video_file):
    with open(output_video_file, 'rb') as op_vid:
        download = download_button.download_button(
            'Download Kick Session',
            data=op_vid,
            file_name='output_live_football.flv',
        )
        if download:
            st.session_state['football_download'] = True

if os.path.exists(output_video_file) and st.session_state['football_download']:
    os.remove(output_video_file)
    st.session_state['football_download'] = False
    download_button.empty()
