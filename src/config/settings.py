"""Application configuration and settings."""
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "disease_dataset.csv")

if not os.path.exists(DATA_FILE):
    DATA_FILE = os.path.join(BASE_DIR, "disease_dataset.csv")

APP_NAME = "MahaArogya Setu"
APP_VERSION = "2.0.0"
MAX_HISTORY_LENGTH = 50
MAX_QUERY_LENGTH = 500

# Gemini Flash Configuration
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
FALLBACK_GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_TIMEOUT_SECONDS = 15

