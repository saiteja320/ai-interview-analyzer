import time

import streamlit as st

from utils.ui import setup_page, disclaimer, step_indicator, ensure_session_defaults, demo_badge
from utils.interview_engine import transcribe
from utils.nlp_analysis import analyze_transcript
from utils.vision_analysis import analyze_facial_expressions, analyze_eye_contact
from utils.feedback_generator import generate_feedback
from data.job_roles import JOB_ROLES

setup_page("Analysis", icon="⚙️")
ensure_session_defaults()
step_indicator(3)

st.title("⚙️ Analysis in Progress")

if not st.session_state.get("answer_media"):
    st.warning("Please complete the Interview step first.")
    if st.button("⬅️ Go to Interview"):
        st.switch_page("pages/2_Interview.py")
    st.stop()

disclaimer()

checklist_placeholder = st.empty()
CHECKLIST_ITEMS = [
    "Resume analyzed",
    "Speech converted to text",
    "Interview answer analyzed",
    "Facial expressions analyzed",
    "Eye contact analyzed",
    "Feedback generated",
]


def render_checklist(done_count: int):
    lines = []
    for i, item in enumerate(CHECKLIST_ITEMS):
        icon = "✅" if i < done_count else ("⏳" if i == done_count else "⬜")
        lines.append(f"{icon} {item}")
    checklist_placeholder.markdown("\n\n".join(lines))


already_done = bool(st.session_state.get("feedback"))

if already_done:
    render_checklist(len(CHECKLIST_ITEMS))
    st.success("Analysis already complete.")
else:
    render_checklist(0)
    time.sleep(0.3)

    # 1. Resume already analyzed on page 1 — mark complete.
    render_checklist(1)
    time.sleep(0.3)

    # 2. Speech to text
    with st.spinner("Transcribing interview answer..."):
        transcription = transcribe(st.session_state.answer_media)
    st.session_state.transcript = transcription["text"]
    st.session_state.transcript_is_demo = transcription["is_demo"]
    render_checklist(2)

    # 3. Transcript analysis
    with st.spinner("Analyzing interview answer..."):
        required_skills = JOB_ROLES[st.session_state.role]["required_skills"]
        transcript_analysis = analyze_transcript(
            st.session_state.transcript, required_skills
        )
    st.session_state.transcript_analysis = transcript_analysis
    render_checklist(3)

    # 4. Facial expression analysis
    with st.spinner("Analyzing facial-expression patterns..."):
        snapshot = st.session_state.get("webcam_snapshot")
        facial_result = analyze_facial_expressions(snapshot)
    st.session_state.facial_result = facial_result
    render_checklist(4)

    # 5. Eye contact analysis
    with st.spinner("Estimating eye-contact indicator..."):
        eye_contact_result = analyze_eye_contact(snapshot)
    st.session_state.eye_contact_result = eye_contact_result
    render_checklist(5)

    # 6. Feedback generation
    with st.spinner("Generating AI feedback..."):
        feedback = generate_feedback(
            st.session_state.match_result,
            transcript_analysis,
            facial_result,
            eye_contact_result,
        )
    st.session_state.feedback = feedback
    render_checklist(6)

    st.success("Analysis complete!")

st.divider()

if st.session_state.get("transcript_is_demo"):
    demo_badge("Speech-to-text is running in demo mode in this environment.")
if st.session_state.get("facial_result", {}).get("is_demo"):
    demo_badge("Facial-expression analysis is running in demo mode.")

if st.button("View Final Report ➡️", type="primary"):
    st.switch_page("pages/4_Final_Report.py")
