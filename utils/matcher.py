"""
Resume-to-job matching.

Computes a match score by blending:
1. Text similarity between resume text and job description (TF-IDF + cosine
   similarity via scikit-learn, if available).
2. Skill overlap ratio between extracted resume skills and the role's
   required skills.

If scikit-learn is not available in the runtime, the module falls back to a
simple word-overlap similarity so the app still works end to end.
"""

import re

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover - fallback path
    SKLEARN_AVAILABLE = False


def _tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z+#.]{2,}", text.lower()))


def _text_similarity(resume_text: str, job_description: str) -> float:
    """Return a 0-1 similarity score between resume text and job description."""
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    if SKLEARN_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf = vectorizer.fit_transform([resume_text, job_description])
            score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
            return float(max(0.0, min(1.0, score)))
        except Exception:
            pass  # fall through to fallback below

    # Fallback: Jaccard similarity over tokens.
    a, b = _tokenize(resume_text), _tokenize(job_description)
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def compute_match(resume_text: str, resume_skills: list, role_name: str,
                   job_description: str, required_skills: list) -> dict:
    """Compute the resume-job match score and matched/missing skill lists.

    The final score blends text similarity (40%) and skill overlap (60%),
    since skill overlap is a more direct, explainable signal for candidates.
    """
    required_skills = [s.lower() for s in required_skills]
    resume_skills_lower = {s.lower() for s in resume_skills}

    matched = sorted(s for s in required_skills if s in resume_skills_lower)
    missing = sorted(s for s in required_skills if s not in resume_skills_lower)

    skill_overlap = (len(matched) / len(required_skills)) if required_skills else 0.0
    text_sim = _text_similarity(resume_text, job_description)

    final_score = 0.6 * skill_overlap + 0.4 * text_sim
    score_pct = round(final_score * 100)

    return {
        "role": role_name,
        "score_pct": score_pct,
        "matched_skills": matched,
        "missing_skills": missing,
        "text_similarity_pct": round(text_sim * 100),
        "skill_overlap_pct": round(skill_overlap * 100),
    }
