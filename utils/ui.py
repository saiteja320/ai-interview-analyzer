"""Shared UI helpers used across all pages for a consistent look and feel."""

import streamlit as st

CUSTOM_CSS = """
<style>
.block-container {padding-top: 2rem; padding-bottom: 3rem;}

.aia-hero {
    background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
    padding: 2.2rem 2rem;
    border-radius: 16px;
    color: white;
    margin-bottom: 1.5rem;
}
.aia-hero h1 {color: white; margin-bottom: 0.3rem;}
.aia-hero p {color: #E0E7FF; font-size: 1.05rem; margin: 0;}

.aia-card {
    background: var(--background-color, #ffffff);
    border: 1px solid rgba(120, 120, 120, 0.18);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.aia-disclaimer {
    background: #FFF7ED;
    border-left: 4px solid #F59E0B;
    padding: 0.8rem 1rem;
    border-radius: 8px;
    font-size: 0.92rem;
    margin-bottom: 1.2rem;
    color: #7C2D12;
}

.aia-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    background: #EEF2FF;
    color: #4338CA;
    font-size: 0.78rem;
    font-weight: 600;
    margin-right: 0.4rem;
}
.aia-badge-demo {
    background: #FEF3C7;
    color: #92400E;
}
</style>
"""


def setup_page(title: str, icon: str = "🤖"):
    st.set_page_config(page_title=f"{title} · AI Interview Analyzer",
                        page_icon=icon, layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    st.markdown(
        f"""<div class="aia-hero"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def disclaimer(text: str = None):
    default = ("This tool provides AI-assisted, decision-support insights only. "
               "It does not determine emotion, confidence, honesty, personality, "
               "or make the final hiring decision — that remains with the human "
               "interviewer/recruiter.")
    st.markdown(f'<div class="aia-disclaimer">⚠️ {text or default}</div>',
                unsafe_allow_html=True)


def demo_badge(label: str):
    st.markdown(f'<span class="aia-badge aia-badge-demo">DEMO MODE</span> '
                f'<span style="font-size:0.85rem;color:#6B7280;">{label}</span>',
                unsafe_allow_html=True)


def step_indicator(current_step: int):
    steps = ["1. Resume", "2. Interview", "3. Analysis", "4. Report"]
    cols = st.columns(len(steps))
    for i, (col, label) in enumerate(zip(cols, steps), start=1):
        with col:
            if i < current_step:
                col.markdown(f"✅ **{label}**")
            elif i == current_step:
                col.markdown(f"🔵 **{label}**")
            else:
                col.markdown(f"⚪ {label}")
    st.divider()


def ensure_session_defaults():
    defaults = {
        "candidate_name": "",
        "role": None,
        "resume_data": None,
        "match_result": None,
        "transcript": "",
        "transcript_is_demo": False,
        "transcript_analysis": None,
        "facial_result": None,
        "eye_contact_result": None,
        "feedback": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
