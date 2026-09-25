import streamlit as st

from utils.ui import setup_page, hero, disclaimer, ensure_session_defaults

setup_page("Home", icon="🤖")
ensure_session_defaults()

hero(
    "AI Interview Analyzer",
    "AI-powered resume and interview analysis — structured insights for "
    "recruiters, useful feedback for candidates.",
)

disclaimer(
    "This is an AI-assisted decision-support prototype, not an automatic "
    "hiring system. Facial expression and eye-contact indicators are "
    "approximate behavioral observations, not measures of emotion, "
    "confidence, honesty, or personality. The final hiring decision always "
    "remains with the human interviewer/recruiter."
)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("What this system does")
    st.markdown(
        """
        Traditional resume screening and initial interview evaluation are
        time-consuming and can be subjective. **AI Interview Analyzer**
        assists — not replaces — that process by:

        1. 📄 Analyzing a candidate's resume against a selected job role
        2. 🎤 Converting a recorded interview answer to text
        3. 🧠 Analyzing the transcript for relevance, keywords, and filler words
        4. 🙂 Estimating observable facial-expression patterns
        5. 👀 Estimating an approximate eye-contact percentage
        6. 📊 Combining everything into a structured feedback report
        """
    )

    st.subheader("Get started")
    bcol1, bcol2 = st.columns(2)
    with bcol1:
        if st.button("🚀 Start Analysis", type="primary", use_container_width=True):
            st.switch_page("pages/1_Resume_Analysis.py")
    with bcol2:
        with st.expander("ℹ️ Learn more"):
            st.markdown(
                """
                **Architecture note:** heavy AI models (Whisper speech-to-text,
                facial-expression classifiers, MediaPipe gaze estimation) are
                wired up behind swappable modules in `utils/`. Where a model
                isn't available in the hosting environment, the app falls
                back to a clearly-labeled **DEMO MODE** output so the full
                pipeline can still be demonstrated end to end.
                """
            )

with col2:
    st.markdown("##### Pipeline")
    st.markdown(
        """
        <div class="aia-card">
        Resume → Job Matching → Interview → Speech-to-Text → NLP Analysis →
        Facial Expression Analysis → Eye Contact Analysis → AI Feedback →
        Final Report
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Built with Streamlit · Python · PyMuPDF · scikit-learn")

st.divider()
st.caption("AI Interview Analyzer — PBL Prototype")
