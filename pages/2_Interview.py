import random

import streamlit as st

from utils.ui import setup_page, disclaimer, step_indicator, ensure_session_defaults
from data.questions import get_questions

setup_page("Interview", icon="🎤")
ensure_session_defaults()
step_indicator(2)

st.title("🎤 Interview")

if not st.session_state.resume_data:
    st.warning("Please complete Resume Analysis first.")
    if st.button("⬅️ Go to Resume Analysis"):
        st.switch_page("pages/1_Resume_Analysis.py")
    st.stop()

disclaimer(
    "Recording and camera capture happen locally in your browser session and "
    "are used only to generate this report."
)

if "current_question" not in st.session_state or not st.session_state.get("current_question"):
    questions = get_questions(st.session_state.role)
    st.session_state.current_question = random.choice(questions)

col_q, col_cam = st.columns([1.3, 1])

with col_q:
    st.subheader("Current Interview Question")
    st.markdown(
        f"""<div class="aia-card" style="font-size:1.2rem;">
        🗨️ {st.session_state.current_question}
        </div>""",
        unsafe_allow_html=True,
    )

    if st.button("🔀 Shuffle Question"):
        questions = get_questions(st.session_state.role)
        st.session_state.current_question = random.choice(questions)
        st.rerun()

    st.subheader("Record / Upload Your Answer")
    st.caption(
        "🔴 In this prototype, record your answer with any voice recorder "
        "app (or your phone) and upload it below — or use your browser mic "
        "if available. In a full version this would be a live start/stop "
        "recorder built with `streamlit-webrtc`."
    )

    audio_answer = None
    if hasattr(st, "audio_input"):
        audio_answer = st.audio_input("🎙️ Record your answer")

    st.markdown("**— or —**")
    uploaded_audio = st.file_uploader(
        "Upload answer audio/video", type=["wav", "mp3", "m4a", "mp4", "mov"]
    )

    final_audio = audio_answer or uploaded_audio
    if final_audio is not None:
        st.audio(final_audio)
        st.session_state.answer_media = final_audio

with col_cam:
    st.subheader("Webcam Snapshot")
    st.caption(
        "Used for facial-expression and eye-contact indicators. A full "
        "version would sample multiple frames throughout the answer."
    )
    snapshot = st.camera_input("Take a snapshot while answering")
    if snapshot is not None:
        st.session_state.webcam_snapshot = snapshot
        st.success("Snapshot captured.")

st.divider()
ready = st.session_state.get("answer_media") is not None
if not ready:
    st.info("Record/upload an answer to continue.")
else:
    if st.button("Submit Answer ➡️", type="primary"):
        st.switch_page("pages/3_Analysis.py")
