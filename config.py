import os
from dotenv import load_dotenv

# Load .env once at the top-level config
load_dotenv()

# Constants with environment fallback
SOURCE_FOLDER = os.getenv("WAV_FOLDER", "./wav_files")
TARGET_FOLDER = os.getenv("MP3_FOLDER", "./converted_mp3")
SUCCESS_FOLDER = os.getenv("SUCCESS_FOLDER", "./success_files")
FAIL_FOLDER = os.getenv("FAIL_FOLDER", "./fail_files")

MIN_DURATION = int(os.getenv("MIN_DURATION", 30))      # seconds
MAX_DURATION = int(os.getenv("MAX_DURATION", 269))     # seconds

API_KEY = os.getenv("MUREKA_API_KEY")
API_BASE = os.getenv("MUREKA_API_BASE", "https://api.mureka.ai")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")