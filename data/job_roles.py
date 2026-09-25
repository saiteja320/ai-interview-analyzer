"""
Sample job roles used for resume-job matching.

Each role has:
- description: a short job description (used for text similarity)
- required_skills: canonical skill list used for skill-overlap matching

This file acts as a stand-in for a real job-postings database. In a full
version this could be loaded from a database or an external API.
"""

JOB_ROLES = {
    "Machine Learning Engineer": {
        "description": (
            "We are looking for a Machine Learning Engineer to design, build, "
            "and deploy ML models. Responsibilities include data preprocessing, "
            "model training, evaluation, and deployment using Python. Experience "
            "with Pandas, NumPy, Scikit-learn, TensorFlow or PyTorch, SQL, and "
            "cloud deployment (Docker, FastAPI, AWS) is required. Strong "
            "understanding of machine learning algorithms, statistics, and "
            "software engineering best practices is expected."
        ),
        "required_skills": [
            "python", "machine learning", "pandas", "numpy", "scikit-learn",
            "tensorflow", "pytorch", "sql", "docker", "fastapi", "git",
            "deep learning", "statistics", "data preprocessing", "aws",
        ],
    },
    "Data Analyst": {
        "description": (
            "We are hiring a Data Analyst to collect, clean, and analyze data "
            "to support business decisions. The ideal candidate is skilled in "
            "SQL, Excel, Python, data visualization (Power BI / Tableau), and "
            "statistical analysis. Strong communication skills and attention "
            "to detail are essential."
        ),
        "required_skills": [
            "sql", "excel", "python", "power bi", "tableau", "statistics",
            "data visualization", "pandas", "data cleaning", "reporting",
        ],
    },
    "Full Stack Developer": {
        "description": (
            "We need a Full Stack Developer proficient in React, JavaScript, "
            "HTML, CSS, Node.js, and REST APIs. Experience with databases "
            "(SQL/NoSQL), Git, and cloud deployment is a plus. You will build "
            "and maintain both frontend and backend components of our web "
            "applications."
        ),
        "required_skills": [
            "react", "javascript", "html", "css", "node.js", "rest api",
            "sql", "git", "mongodb", "express", "typescript",
        ],
    },
    "Software Engineer": {
        "description": (
            "We are seeking a Software Engineer with strong problem-solving "
            "skills and experience in data structures, algorithms, and object "
            "oriented programming. Proficiency in at least one of Python, "
            "Java, or C++ is required, along with familiarity with Git, unit "
            "testing, and REST APIs."
        ),
        "required_skills": [
            "python", "java", "c++", "data structures", "algorithms", "git",
            "oop", "rest api", "unit testing", "sql",
        ],
    },
    "AI/NLP Engineer": {
        "description": (
            "We are looking for an AI/NLP Engineer to build natural language "
            "processing pipelines. Experience with spaCy, NLTK, Sentence "
            "Transformers, Hugging Face Transformers, Python, and deep "
            "learning frameworks is required. Familiarity with speech "
            "processing (Whisper) and computer vision (OpenCV) is a plus."
        ),
        "required_skills": [
            "python", "nlp", "spacy", "nltk", "transformers",
            "sentence transformers", "pytorch", "opencv", "whisper",
            "machine learning", "deep learning",
        ],
    },
}

# Flat master skill vocabulary used by the resume parser to detect skills
# even for roles/resumes that mention things outside a specific role list.
MASTER_SKILL_LIST = sorted(
    {skill for role in JOB_ROLES.values() for skill in role["required_skills"]}
    | {
        "django", "flask", "kubernetes", "linux", "azure", "gcp",
        "matplotlib", "seaborn", "keras", "opencv", "mediapipe",
        "html", "css", "c", "communication", "leadership", "teamwork",
    }
)
