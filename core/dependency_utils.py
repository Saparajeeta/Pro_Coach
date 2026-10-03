from pathlib import Path

try:
    import av
    from aiortc.contrib.media import MediaRecorder
    from streamlit_webrtc import VideoHTMLAttributes, webrtc_streamer
except Exception as exc:  # pragma: no cover - surfaced when dependencies are missing
    raise ModuleNotFoundError(
        "The webcam dependencies for the sports pages are missing. Install the project requirements first."
    ) from exc


def project_path(filename: str) -> str:
    return str(Path(__file__).resolve().parents[1] / filename)


def load_webrtc_dependencies(module_name: str):
    return av, VideoHTMLAttributes, webrtc_streamer, MediaRecorder
