"""
Interview transcript analysis.

Uses lightweight, dependency-free heuristics so the app runs on any hosting
tier:
- Relevance: token/skill overlap between the transcript and the target
  job's required skills + description (swap in Sentence-Transformers
  embeddings later for semantic similarity behind the same function shape).
- Filler word count: regex match against a common filler-word list.
- Keyword extraction: overlap with the master skill vocabulary.
- Answer length: word count and a rough estimated speaking duration.
"""

import re

from data.job_roles import MASTER_SKILL_LIST

FILLER_WORDS = [
    "um", "uh", "like", "you know", "basically", "actually", "so",
    "kind of", "sort of", "i mean", "literally", "right",
]

WORDS_PER_MINUTE = 130  # rough average conversational speaking rate


def _count_fillers(text: str) -> int:
    text_lower = text.lower()
    count = 0
    for filler in FILLER_WORDS:
        pattern = r"(?<![a-zA-Z])" + re.escape(filler) + r"(?![a-zA-Z])"
        count += len(re.findall(pattern, text_lower))
    return count


def _extract_keywords(text: str) -> list:
    text_lower = text.lower()
    found = []
    for skill in MASTER_SKILL_LIST:
        pattern = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))


def _relevance_score(transcript_keywords: list, required_skills: list) -> str:
    if not required_skills:
        return "N/A"
    required_lower = {s.lower() for s in required_skills}
    overlap = len(set(transcript_keywords) & required_lower)
    ratio = overlap / len(required_lower)
    if ratio >= 0.5:
        return "High"
    elif ratio >= 0.2:
        return "Medium"
    return "Low"


def analyze_transcript(transcript: str, required_skills: list) -> dict:
    """Analyze an interview transcript and return structured indicators."""
    if not transcript.strip():
        return {
            "relevance": "N/A",
            "keywords": [],
            "word_count": 0,
            "estimated_seconds": 0,
            "filler_word_count": 0,
        }

    words = re.findall(r"[a-zA-Z']+", transcript)
    word_count = len(words)
    estimated_seconds = round((word_count / WORDS_PER_MINUTE) * 60)

    keywords = _extract_keywords(transcript)
    relevance = _relevance_score(keywords, required_skills)
    filler_count = _count_fillers(transcript)

    return {
        "relevance": relevance,
        "keywords": keywords,
        "word_count": word_count,
        "estimated_seconds": estimated_seconds,
        "filler_word_count": filler_count,
    }
