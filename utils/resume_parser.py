"""
Resume parsing utilities.

Extracts raw text from an uploaded PDF resume using PyMuPDF, then pulls out
skills, education, experience, projects, and certifications using
lightweight rule-based heuristics (keyword matching + section detection).

This module is intentionally dependency-light so the app can run on
Streamlit Community Cloud without heavyweight NLP models. It is structured
so a real NLP-based resume parser (e.g. spaCy NER, a fine-tuned model) can
be swapped in later behind the same function signatures.
"""

import io
import re

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:  # pragma: no cover - fallback path
    PYMUPDF_AVAILABLE = False

from data.job_roles import MASTER_SKILL_LIST

SECTION_HEADERS = {
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "work experience", "employment history",
                   "professional experience"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certifications": ["certifications", "certificates", "licenses"],
}


def extract_text_from_pdf(uploaded_file) -> str:
    """Extract raw text from an uploaded PDF file-like object.

    Returns an empty string (with no exception) if extraction fails, so the
    UI can show a friendly error instead of crashing.
    """
    if uploaded_file is None:
        return ""

    file_bytes = uploaded_file.read()
    # Reset pointer in case the caller needs to re-read the uploaded file.
    try:
        uploaded_file.seek(0)
    except Exception:
        pass

    if not PYMUPDF_AVAILABLE:
        return ""

    try:
        text_parts = []
        with fitz.open(stream=io.BytesIO(file_bytes), filetype="pdf") as doc:
            for page in doc:
                text_parts.append(page.get_text())
        return "\n".join(text_parts)
    except Exception:
        return ""


def _find_section(text: str, headers: list) -> str:
    """Return the text block following the first matching section header,
    up to the next section header (or end of document)."""
    lines = text.splitlines()
    lowered = [line.strip().lower() for line in lines]

    start_idx = None
    for i, line in enumerate(lowered):
        if any(line.startswith(h) or line == h for h in headers):
            start_idx = i + 1
            break
    if start_idx is None:
        return ""

    all_headers = [h for group in SECTION_HEADERS.values() for h in group]
    end_idx = len(lines)
    for i in range(start_idx, len(lowered)):
        if any(lowered[i].startswith(h) for h in all_headers) and lowered[i]:
            end_idx = i
            break

    return "\n".join(lines[start_idx:end_idx]).strip()


def extract_skills(text: str) -> list:
    """Detect known skills mentioned in the resume text (case-insensitive,
    whole-word / whole-phrase match)."""
    if not text:
        return []
    text_lower = text.lower()
    found = []
    for skill in MASTER_SKILL_LIST:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def extract_education(text: str) -> str:
    section = _find_section(text, SECTION_HEADERS["education"])
    return section if section else "Not clearly detected — please review resume manually."


def extract_experience(text: str) -> str:
    section = _find_section(text, SECTION_HEADERS["experience"])
    return section if section else "Not clearly detected — may be an entry-level / student resume."


def extract_projects(text: str) -> str:
    section = _find_section(text, SECTION_HEADERS["projects"])
    return section if section else "Not clearly detected — please review resume manually."


def extract_certifications(text: str) -> str:
    section = _find_section(text, SECTION_HEADERS["certifications"])
    return section if section else "None detected."


def parse_resume(uploaded_file) -> dict:
    """Run the full resume parsing pipeline and return a structured dict."""
    text = extract_text_from_pdf(uploaded_file)
    return {
        "raw_text": text,
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
        "projects": extract_projects(text),
        "certifications": extract_certifications(text),
        "extraction_ok": bool(text.strip()),
    }
