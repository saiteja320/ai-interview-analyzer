# 🤖 AI Interview Analyzer

An AI-assisted decision-support prototype for resume screening and initial
interview evaluation, built for a PBL (Project-Based Learning) submission.

> **Important:** This is a decision-**support** tool. It does not determine
> emotion, confidence, honesty, or personality, and it never makes the final
> hiring decision — that stays with the human interviewer/recruiter.

---

## ✨ Features

| Stage | What it does |
|---|---|
| 📄 Resume Analysis | Upload a PDF resume, select/describe a job role, get a resume-job match score with matched/missing skills |
| 🎤 Interview | View a role-specific interview question, record/upload an answer, capture a webcam snapshot |
| 🧠 Speech-to-Text | Transcribes the answer (real Whisper if available, otherwise a clearly-labeled demo transcript) |
| 📊 Answer Analysis | Relevance, keywords, filler-word count, answer length |
| 🙂 Visual Analysis | Observed facial-expression distribution and an approximate eye-contact percentage |
| ✅ AI Feedback | Rule-based strengths / areas for improvement / recommendations |
| 📑 Final Report | Professional dashboard report, downloadable as Markdown |

---

## 🏗️ Architecture

```
app.py                      → Landing page
pages/
  1_Resume_Analysis.py      → Upload resume, select role, run matching
  2_Interview.py            → Show question, record answer, webcam snapshot
  3_Analysis.py             → Runs the full pipeline with progress indicators
  4_Final_Report.py         → Dashboard report + Markdown download
utils/
  resume_parser.py          → PDF text extraction + section/skill extraction
  matcher.py                → TF-IDF + skill-overlap resume-job matching
  interview_engine.py       → Speech-to-text (Whisper, with demo fallback)
  nlp_analysis.py           → Transcript relevance / keywords / filler words
  vision_analysis.py        → Facial-expression + eye-contact (demo fallback)
  feedback_generator.py     → Combines everything into structured feedback
  report.py                 → Builds the downloadable Markdown report
  ui.py                     → Shared styling / layout helpers
data/
  job_roles.py               → Sample job roles, descriptions, required skills
  questions.py                → Sample interview question bank per role
```

Each analysis module is **independent and swappable** — every function
returns the same shape whether it's backed by a real model or a demo
fallback, so wiring in real Whisper / OpenCV / MediaPipe models later (e.g.
behind a FastAPI backend, per the original spec) requires no changes to the
pages or the feedback/report logic.

### About "DEMO MODE"

Whisper, OpenCV facial-expression models, and MediaPipe are heavy
dependencies (large downloads, GPU-friendly, slow cold starts) that often
don't fit free hosting tiers like Streamlit Community Cloud. By default this
app runs with those dependencies **commented out** in `requirements.txt` and
falls back to clearly-labeled demo output for those specific stages, while
the resume parsing and matching (PyMuPDF + scikit-learn) run for real. To
enable real speech-to-text / vision models, uncomment the optional
dependencies in `requirements.txt` and deploy somewhere with enough
CPU/RAM (Whisper + MediaPipe are unlikely to fit the free Streamlit Cloud
tier).

---

## 🚀 Run locally

```bash
# 1. Clone your repo (after you've pushed it — see below)
git clone https://github.com/<your-username>/ai-interview-analyzer.git
cd ai-interview-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## ☁️ Push to GitHub

From inside the `ai-interview-analyzer` folder:

```bash
git init
git add .
git commit -m "Initial commit: AI Interview Analyzer prototype"
git branch -M main
git remote add origin https://github.com/<your-username>/ai-interview-analyzer.git
git push -u origin main
```

(Create the empty repo on GitHub first if you haven't — no README/license,
since you already have one locally, to avoid a merge conflict on first push.)

---

## 🌐 Deploy on Streamlit Community Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.
2. Click **"New app"**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Click **Deploy**.

Streamlit Cloud will install everything in `requirements.txt` and launch the
app. Any future `git push` to `main` will automatically redeploy it.

---

## 🎓 PBL Notes

- This is a **prototype**, not a production hiring system.
- Sections marked *DEMO MODE* in the UI indicate simulated output where a
  heavy real-time AI model wasn't practical for this environment — the
  surrounding architecture (data flow, module boundaries) is built exactly
  as it would be for the real models, per the "modular, swap-in-ready"
  requirement in the project brief.
- Feel free to extend `data/job_roles.py` and `data/questions.py` with more
  roles/questions for your demo.
