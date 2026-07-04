import os
import secrets
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    if not SECRET_KEY:
        # Fallback to a random key if not configured in the environment
        SECRET_KEY = secrets.token_hex(24)

    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    PORT = int(os.getenv("FLASK_PORT", "5001"))

    # Instagram Integration Settings
    # Supports 'mock' (default) or 'graph'
    PROVIDER = os.getenv("INSTAGRAM_PROVIDER", "mock").lower()
    ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")

    # Ensure provider option is valid
    if PROVIDER not in ("mock", "graph"):
        raise ValueError(f"Invalid INSTAGRAM_PROVIDER: {PROVIDER}. Must be 'mock' or 'graph'.")
