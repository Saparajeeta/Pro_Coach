import streamlit as st
from streamlit.components.v1 import html


def render_view_controls(key_prefix):
    view_size = st.radio(
        "View size",
        ["Small (40%)", "Half (50%)", "Large (75%)", "Full width (100%)"],
        index=1,
        horizontal=True,
        key=f"{key_prefix}_view_size",
    )
    voice_enabled = st.checkbox("Voice feedback", value=True, key=f"{key_prefix}_voice")
    try:
        import audio_feedback
        audio_feedback.set_voice_enabled(voice_enabled)
    except Exception:
        pass
    st.caption("Choose the size before pressing Start. Changing it while streaming may restart the camera.")

    if view_size == "Small (40%)":
        col = st.columns([3, 4, 3])[1]
    elif view_size == "Half (50%)":
        col = st.columns([1, 2, 1])[1]
    elif view_size == "Large (75%)":
        col = st.columns([1, 6, 1])[1]
    else:
        col = st.columns([1])[0]

    if st.button("Full screen"):
        try:
            html(
                """
                <script>
                try {
                    const video = window.parent.document.querySelector('video');
                    if (video && typeof video.requestFullscreen === 'function') {
                        video.requestFullscreen();
                    }
                } catch (e) {}
                </script>
                """,
                height=0,
            )
        except Exception:
            pass
    return col
