import streamlit as st

from utils.ui import setup_page, disclaimer, step_indicator, ensure_session_defaults, hero
from utils.report import build_report_markdown

setup_page("Final Report", icon="📊")
ensure_session_defaults()
step_indicator(4)

if not st.session_state.get("feedback"):
    st.warning("Please complete the Analysis step first.")
    if st.button("⬅️ Go to Analysis"):
        st.switch_page("pages/3_Analysis.py")
    st.stop()

hero("AI INTERVIEW ANALYZER", "Final Interview Report")
disclaimer(
    "This report is an AI-assisted summary for decision SUPPORT. It is not "
    "a hiring decision. Facial-expression and eye-contact figures are "
    "approximate behavioral indicators only."
)

candidate = st.session_state.candidate_name or "Candidate"
role = st.session_state.role
match_result = st.session_state.match_result
transcript_analysis = st.session_state.transcript_analysis
facial_result = st.session_state.facial_result
eye_contact_result = st.session_state.eye_contact_result
feedback = st.session_state.feedback

st.markdown(f"### Candidate: {candidate}")
st.markdown(f"**Target Role:** {role}")

m1, m2, m3 = st.columns(3)
m1.metric("Resume Match", f"{match_result['score_pct']}%")
m2.metric("Eye Contact", f"{eye_contact_result.get('eye_contact_pct', 0)}%")
m3.metric("Answer Relevance", transcript_analysis.get("relevance", "N/A"))

st.divider()

tab_resume, tab_interview, tab_visual, tab_feedback = st.tabs(
    ["📄 Resume Analysis", "🎤 Interview Analysis", "👁️ Visual Analysis", "🧠 AI Feedback"]
)

with tab_resume:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**✅ Matched Skills**")
        for s in match_result["matched_skills"]:
            st.markdown(f"- ✓ {s}")
        if not match_result["matched_skills"]:
            st.caption("None detected")
    with c2:
        st.markdown("**❌ Missing Skills**")
        for s in match_result["missing_skills"]:
            st.markdown(f"- ✗ {s}")
        if not match_result["missing_skills"]:
            st.caption("None — full coverage!")

    resume_data = st.session_state.resume_data
    if resume_data:
        st.markdown("**Projects**")
        st.text(resume_data["projects"])
        st.markdown("**Experience**")
        st.text(resume_data["experience"])

with tab_interview:
    if st.session_state.get("transcript_is_demo"):
        st.caption("⚠️ DEMO MODE transcript — Whisper not available in this environment.")
    st.markdown("**Transcript**")
    st.markdown(f'<div class="aia-card">{st.session_state.transcript}</div>',
                unsafe_allow_html=True)

    st.markdown("**Keywords**")
    kw = transcript_analysis.get("keywords", [])
    st.write(", ".join(kw) if kw else "None detected")

    c1, c2, c3 = st.columns(3)
    c1.metric("Relevance", transcript_analysis.get("relevance", "N/A"))
    c2.metric("Answer Length", f"{transcript_analysis.get('estimated_seconds', 0)}s")
    c3.metric("Filler Words", transcript_analysis.get("filler_word_count", 0))

with tab_visual:
    if facial_result.get("is_demo"):
        st.caption("⚠️ DEMO MODE — simulated output, not a real CV model.")
    st.markdown("**Facial Expression Distribution**")
    dist = facial_result.get("distribution", {})
    for label, pct in dist.items():
        st.write(f"{label}")
        st.progress(pct / 100)
        st.caption(f"{pct}%")

    st.markdown("**Eye Contact**")
    ec = eye_contact_result.get("eye_contact_pct", 0)
    st.write(f"Looking toward camera: {ec}%")
    st.progress(ec / 100)
    st.write(f"Looking away: {eye_contact_result.get('looking_away_pct', 0)}%")

with tab_feedback:
    st.markdown("#### 💪 Strengths")
    for s in feedback["strengths"]:
        st.markdown(f"- {s}")
    st.markdown("#### 📈 Areas for Improvement")
    for i in feedback["improvements"]:
        st.markdown(f"- {i}")
    st.markdown("#### 🎯 Recommendations")
    for r in feedback["recommendations"]:
        st.markdown(f"- {r}")

st.divider()

report_md = build_report_markdown({
    "candidate_name": candidate,
    "role": role,
    "match_result": match_result,
    "transcript": st.session_state.transcript,
    "transcript_is_demo": st.session_state.transcript_is_demo,
    "transcript_analysis": transcript_analysis,
    "facial_result": facial_result,
    "eye_contact_result": eye_contact_result,
    "feedback": feedback,
})

dl1, dl2 = st.columns([1, 3])
with dl1:
    st.download_button(
        "⬇️ Download Report",
        data=report_md,
        file_name=f"interview_report_{candidate.replace(' ', '_') or 'candidate'}.md",
        mime="text/markdown",
        type="primary",
        use_container_width=True,
    )
with dl2:
    if st.button("🔄 Start New Analysis"):
        for key in ["resume_data", "match_result", "transcript", "transcript_is_demo",
                    "transcript_analysis", "facial_result", "eye_contact_result",
                    "feedback", "answer_media", "webcam_snapshot", "current_question"]:
            st.session_state.pop(key, None)
        st.switch_page("app.py")
