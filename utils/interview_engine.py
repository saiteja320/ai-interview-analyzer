"""
Interview speech-to-text engine.

Wraps OpenAI's Whisper model behind a single `transcribe()` function. Whisper
is a large dependency (needs torch + ffmpeg) that is often impractical on
free-tier hosting like Streamlit Community Cloud, so this module:

1. Tries to use a real local Whisper model if the `whisper` package and
   ffmpeg are available in the runtime.
2. Falls back to a clearly-labeled DEMO transcript otherwise, so the rest of
   the pipeline (NLP analysis, feedback, report) still runs end to end.

Swap in a hosted Whisper API call here later without touching any other
module — every other module only depends on this function's return shape.
"""

import random

DEMO_MODE_LABEL = "[DEMO MODE — Whisper not available in this environment]"

_DEMO_TRANSCRIPTS = [
    (
        "Hello, my name is Sai Teja. I am a Computer Science student with a "
        "strong interest in Machine Learning. I have worked on projects "
        "involving Python, Pandas, and Scikit-learn, including a resume "
        "screening tool and a student performance predictor. I enjoy solving "
        "real-world problems with data and I'm looking for an opportunity to "
        "apply my skills in a production environment."
    ),
    (
        "In my last project, I built an end-to-end machine learning pipeline "
        "using Python and Scikit-learn. I handled data cleaning with Pandas, "
        "trained a classification model, and evaluated it using cross "
        "validation. I also containerized the application using Docker and "
        "exposed it through a FastAPI endpoint. One challenge I faced was "
        "class imbalance in the dataset, which I addressed using SMOTE."
    ),
    (
        "I would describe myself as a fast learner and a team player. During "
        "my final year project, I collaborated with three other students to "
        "build a web application. My role was mainly the backend and data "
        "processing logic. We used Git for version control and had weekly "
        "stand-ups to track progress, which taught me a lot about "
        "communication under deadlines."
    ),
]


def _load_whisper_model():
    """Attempt to load a real Whisper model. Returns None if unavailable."""
    try:
        import whisper  # noqa: F401
        model = whisper.load_model("base")
        return model
    except Exception:
        return None


def transcribe(audio_file) -> dict:
    """Transcribe an uploaded audio/video answer.

    Returns:
        {
            "text": str,
            "is_demo": bool,
            "source_label": str,
        }
    """
    if audio_file is None:
        return {"text": "", "is_demo": True, "source_label": DEMO_MODE_LABEL}

    model = _load_whisper_model()

    if model is not None:
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                tmp.write(audio_file.read())
                tmp_path = tmp.name
            result = model.transcribe(tmp_path)
            return {
                "text": result.get("text", "").strip(),
                "is_demo": False,
                "source_label": "Transcribed with Whisper",
            }
        except Exception:
            pass  # fall through to demo mode below

    # Demo fallback — clearly labeled, never presented as real output.
    demo_text = random.choice(_DEMO_TRANSCRIPTS)
    return {"text": demo_text, "is_demo": True, "source_label": DEMO_MODE_LABEL}
