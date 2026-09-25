import streamlit as st

from utils.ui import setup_page, disclaimer, step_indicator, ensure_session_defaults
from utils.resume_parser import parse_resume
from utils.matcher import compute_match
from data.job_roles import JOB_ROLES

setup_page("Resume Analysis", icon="📄")
ensure_session_defaults()
step_indicator(1)

st.title("📄 Resume Analysis")
disclaimer("Resume parsing uses rule-based text extraction. Always double-check "
           "extracted sections against the original resume.")

col_form, col_result = st.columns([1, 1.3])

with col_form:
    st.subheader("Candidate & Role")
    st.session_state.candidate_name = st.text_input(
        "Candidate Name", value=st.session_state.candidate_name or "",
        placeholder="e.g. Sai Teja",
    )

    role = st.selectbox("Target Job Role", options=list(JOB_ROLES.keys()),
                         index=list(JOB_ROLES.keys()).index(st.session_state.role)
                         if st.session_state.role in JOB_ROLES else 0)
    st.session_state.role = role

    default_jd = JOB_ROLES[role]["description"]
    job_description = st.text_area(
        "Job Description", value=default_jd, height=160,
        help="Pre-filled with a sample description for the selected role — edit freely.",
    )

    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    analyze_clicked = st.button("🔍 Analyze Resume", type="primary",
                                 use_container_width=True)

    if analyze_clicked:
        if uploaded_resume is None:
            st.error("Please upload a resume PDF first.")
        else:
            with st.spinner("Extracting resume content..."):
                resume_data = parse_resume(uploaded_resume)
            if not resume_data["extraction_ok"]:
                st.warning(
                    "Could not extract text from this PDF (it may be a "
                    "scanned image without a text layer). Try a text-based "
                    "PDF export of the resume."
                )
            st.session_state.resume_data = resume_data

            match_result = compute_match(
                resume_text=resume_data["raw_text"],
                resume_skills=resume_data["skills"],
                role_name=role,
                job_description=job_description,
                required_skills=JOB_ROLES[role]["required_skills"],
            )
            st.session_state.match_result = match_result
            st.success("Resume analyzed successfully.")

with col_result:
    st.subheader("Results")
    resume_data = st.session_state.resume_data
    match_result = st.session_state.match_result

    if not resume_data:
        st.info("Upload a resume and click **Analyze Resume** to see results here.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Resume Match Score", f"{match_result['score_pct']}%")
        m2.metric("Skill Overlap", f"{match_result['skill_overlap_pct']}%")
        m3.metric("Text Similarity", f"{match_result['text_similarity_pct']}%")

        st.progress(match_result["score_pct"] / 100)

        tab1, tab2, tab3 = st.tabs(["Skills", "Sections", "Raw Text"])

        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**✅ Matched Skills**")
                if match_result["matched_skills"]:
                    for s in match_result["matched_skills"]:
                        st.markdown(f"- ✓ {s}")
                else:
                    st.caption("None detected")
            with c2:
                st.markdown("**❌ Missing Skills**")
                if match_result["missing_skills"]:
                    for s in match_result["missing_skills"]:
                        st.markdown(f"- ✗ {s}")
                else:
                    st.caption("None — full coverage!")

        with tab2:
            st.markdown("**Education**")
            st.text(resume_data["education"])
            st.markdown("**Experience**")
            st.text(resume_data["experience"])
            st.markdown("**Projects**")
            st.text(resume_data["projects"])
            st.markdown("**Certifications**")
            st.text(resume_data["certifications"])

        with tab3:
            st.text_area("Extracted Text", value=resume_data["raw_text"],
                          height=250, disabled=True)

        st.divider()
        if st.button("Next: Start Interview ➡️", type="primary"):
            st.switch_page("pages/2_Interview.py")
