from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = BASE_DIR / "config"
THEME_CSS_PATH = CONFIG_DIR / "theme.css"
DISEASE_DATASET_CSV = BASE_DIR / "disease_dataset.csv"

# Streamlit Page Config
PAGE_CONFIG = {
    "page_title": "MahaArogya Setu — Rural Healthcare Access Platform | SIH",
    "page_icon": "🩺",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# Dataset Columns
REQUIRED_COLUMNS = ["disease", "symptoms", "prevention", "when_to_see_doctor", "home_care"]
ENHANCED_COLUMNS = [
    "severity",
    "age_group",
    "category",
    "rural_prevalence",
    "govt_free_treatment",
    "recommended_facility",
]

# Language Modes
MODE_ENGLISH = "English"
MODE_HINDI = "हिंदी (Hindi)"
MODE_MARATHI = "मराठी (Marathi)"
MODE_AUTO = "🌐 Auto-detect"
LANGUAGES = [MODE_ENGLISH, MODE_HINDI, MODE_MARATHI, MODE_AUTO]

# NLP Constants
STOPWORDS = {
    "a", "an", "the", "and", "or", "in", "of", "with", "for", "to", "my", "me", "i",
    "i'm", "im", "have", "has", "had", "is", "are", "was", "were", "am", "it", "this",
    "that", "some", "someone", "feeling", "feel", "got", "get",
}
GENERIC_SYMPTOMS = {
    "fever", "pain", "cough", "fatigue", "headache", "weakness", "rash", "nausea",
    "vomiting", "cold", "ache", "tired", "tiredness", "sick",
}
STEM_EXCEPTIONS = {"aches": "ache", "headaches": "headache", "stomachaches": "stomachache"}
COMPOUND_ACHE_WORDS = ("head", "body", "ear", "stomach", "tooth", "back", "neck", "belly")
