"""
AI feedback generator.

Combines resume match, transcript analysis, facial-expression indicators,
and eye-contact indicators into structured, rule-based feedback: strengths,
areas for improvement, and specific recommendations.

This is a decision-SUPPORT tool. It intentionally never outputs a hire /
no-hire verdict — see Section 15 of the project brief. A real version could
replace the rule-based logic below with an LLM call that takes the same
inputs and returns the same three lists.
"""


def generate_feedback(match_result: dict, transcript_analysis: dict,
                       facial_result: dict, eye_contact_result: dict) -> dict:
    strengths = []
    improvements = []
    recommendations = []

    # --- Resume / skill match ---
    score = match_result.get("score_pct", 0)
    matched = match_result.get("matched_skills", [])
    missing = match_result.get("missing_skills", [])

    if score >= 75:
        strengths.append("Strong overall resume-job alignment.")
    elif score >= 45:
        improvements.append("Moderate resume-job alignment — consider tailoring the resume further to the role.")
    else:
        improvements.append("Low resume-job alignment for this specific role.")

    if matched:
        strengths.append(f"Strong coverage of key required skills: {', '.join(matched[:5])}.")
    if missing:
        improvements.append(f"Missing job-specific skills: {', '.join(missing[:5])}.")
        recommendations.append(f"Consider building a small project or certification covering: {', '.join(missing[:3])}.")

    # --- Transcript / answer quality ---
    relevance = transcript_analysis.get("relevance", "N/A")
    filler_count = transcript_analysis.get("filler_word_count", 0)
    word_count = transcript_analysis.get("word_count", 0)

    if relevance == "High":
        strengths.append("Interview answer was highly relevant to the target role.")
    elif relevance == "Medium":
        improvements.append("Interview answer was only partially relevant — tie responses more directly to the role's required skills.")
    elif relevance == "Low":
        improvements.append("Interview answer had low relevance to the target role's required skills.")

    if filler_count >= 6:
        improvements.append(f"Frequent filler words detected ({filler_count}) — this can reduce perceived clarity.")
        recommendations.append("Practice answers out loud and pause instead of using filler words like 'um' or 'like'.")
    elif filler_count <= 2 and word_count > 0:
        strengths.append("Clear, concise delivery with minimal filler words.")

    if word_count > 0 and word_count < 25:
        improvements.append("Answer was quite short — consider elaborating with a specific example (situation, action, result).")
        recommendations.append("Use the STAR method (Situation, Task, Action, Result) to structure longer answers.")

    # --- Visual indicators (explicitly framed as approximate) ---
    eye_pct = eye_contact_result.get("eye_contact_pct", 0)
    if eye_pct >= 70:
        strengths.append(f"Consistent camera attention observed (~{eye_pct}%).")
    elif eye_pct > 0:
        improvements.append(f"Camera attention was lower than ideal (~{eye_pct}%).")
        recommendations.append("Practice maintaining steady attention toward the camera during video interviews.")

    distribution = facial_result.get("distribution", {})
    if distribution:
        dominant = max(distribution, key=distribution.get)
        if dominant == "Neutral" and distribution[dominant] > 70:
            recommendations.append("Try to show a little more engagement/expressiveness — an overly neutral expression can read as disengaged.")

    if not strengths:
        strengths.append("Completed all stages of the interview process.")
    if not recommendations:
        recommendations.append("Continue practicing mock interviews focused on this role's required skills.")

    return {
        "strengths": strengths,
        "improvements": improvements,
        "recommendations": recommendations,
    }
