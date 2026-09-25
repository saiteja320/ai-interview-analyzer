"""
Sample interview question bank, organized by job role.

In a production system this could be generated dynamically (e.g. from the
job description and resume) rather than hard-coded.
"""

INTERVIEW_QUESTIONS = {
    "Machine Learning Engineer": [
        "Tell me about yourself and your experience with machine learning.",
        "Walk me through a machine learning project you have built end to end.",
        "How do you handle overfitting in a model?",
        "Explain the difference between supervised and unsupervised learning.",
        "How would you deploy a trained model into production?",
    ],
    "Data Analyst": [
        "Tell me about yourself and your experience with data analysis.",
        "Describe a time you used data to influence a business decision.",
        "How do you handle missing or inconsistent data?",
        "What is the difference between a JOIN and a UNION in SQL?",
        "How do you decide which chart to use for a given dataset?",
    ],
    "Full Stack Developer": [
        "Tell me about yourself and your development background.",
        "Describe a full stack project you have worked on.",
        "How do you manage state in a React application?",
        "Explain how you would design a REST API for a to-do app.",
        "How do you approach debugging a production issue?",
    ],
    "Software Engineer": [
        "Tell me about yourself and your programming background.",
        "Describe a challenging bug you fixed and how you approached it.",
        "Explain the time complexity of your favorite sorting algorithm.",
        "How do you approach writing unit tests for new code?",
        "Tell me about a time you worked in a team on a software project.",
    ],
    "AI/NLP Engineer": [
        "Tell me about yourself and your experience with NLP.",
        "Explain how a transformer model processes text.",
        "Describe a project where you built an NLP pipeline.",
        "How would you evaluate the quality of a text classification model?",
        "What challenges have you faced with noisy or unstructured text data?",
    ],
}

DEFAULT_QUESTIONS = [
    "Tell me about yourself.",
    "Describe a project you are proud of.",
    "What are your key technical strengths?",
    "How do you handle challenges or setbacks?",
    "Why are you a good fit for this role?",
]


def get_questions(role: str):
    """Return the question list for a role, falling back to defaults."""
    return INTERVIEW_QUESTIONS.get(role, DEFAULT_QUESTIONS)
