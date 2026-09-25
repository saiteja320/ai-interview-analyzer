"""
Facial expression and eye-contact analysis.

Real facial-expression and gaze-estimation models (OpenCV + a pretrained
expression classifier, MediaPipe Face Mesh) are heavy dependencies that may
not be available in every hosting environment. This module tries to use
OpenCV / MediaPipe if present, and otherwise produces a clearly-labeled
DEMO estimate derived deterministically from the uploaded file (so re-runs
on the same file are stable, unlike pure random noise).

IMPORTANT (see Section 15 of the project brief): these are observable,
approximate behavioral indicators only. They do not measure or prove a
person's real emotions, confidence, honesty, or personality, and they must
never be used to make an automated hiring decision.
"""

import hashlib

try:
    import cv2  # noqa: F401
    OPENCV_AVAILABLE = True
except ImportError:  # pragma: no cover
    OPENCV_AVAILABLE = False

try:
    import mediapipe as mp  # noqa: F401
    MEDIAPIPE_AVAILABLE = True
except ImportError:  # pragma: no cover
    MEDIAPIPE_AVAILABLE = False

DEMO_LABEL = "[DEMO MODE — observed pattern is simulated, not a real CV model]"


def _stable_seed(file_bytes: bytes) -> int:
    """Derive a stable pseudo-random seed from file content so repeated
    analysis of the same upload gives consistent demo numbers."""
    digest = hashlib.sha256(file_bytes).hexdigest()
    return int(digest[:8], 16)


def analyze_facial_expressions(media_file) -> dict:
    """Return an observed facial-expression distribution.

    Returns:
        {
            "distribution": {"Neutral": .., "Happy": .., ...},  # sums to 100
            "is_demo": bool,
            "label": str,
        }
    """
    if media_file is None:
        return {"distribution": {}, "is_demo": True, "label": DEMO_LABEL}

    file_bytes = media_file.read()
    try:
        media_file.seek(0)
    except Exception:
        pass

    if OPENCV_AVAILABLE:
        # Placeholder hook: a real implementation would decode frames with
        # cv2, run a pretrained facial-expression classifier per frame, and
        # aggregate the distribution here. Left as demo mode until a real
        # model is wired in, per Section 14 of the brief.
        pass

    seed = _stable_seed(file_bytes)
    neutral = 45 + (seed % 25)              # 45-69
    happy = 10 + ((seed >> 8) % 25)          # 10-34
    remainder = max(0, 100 - neutral - happy)
    surprise = remainder // 2
    sad = remainder - surprise

    distribution = {
        "Neutral": neutral,
        "Happy": happy,
        "Surprise": surprise,
        "Sad": sad,
    }
    return {"distribution": distribution, "is_demo": True, "label": DEMO_LABEL}


def analyze_eye_contact(media_file) -> dict:
    """Return an estimated eye-contact percentage.

    Returns:
        {
            "eye_contact_pct": int,
            "looking_away_pct": int,
            "is_demo": bool,
            "label": str,
        }
    """
    if media_file is None:
        return {"eye_contact_pct": 0, "looking_away_pct": 0,
                 "is_demo": True, "label": DEMO_LABEL}

    file_bytes = media_file.read()
    try:
        media_file.seek(0)
    except Exception:
        pass

    if MEDIAPIPE_AVAILABLE and OPENCV_AVAILABLE:
        # Placeholder hook: a real implementation would run MediaPipe Face
        # Mesh per frame, estimate gaze direction relative to the camera,
        # and compute the percentage of frames looking toward the camera.
        pass

    seed = _stable_seed(file_bytes)
    eye_contact_pct = 55 + (seed % 35)  # 55-89
    return {
        "eye_contact_pct": eye_contact_pct,
        "looking_away_pct": 100 - eye_contact_pct,
        "is_demo": True,
        "label": DEMO_LABEL,
    }
