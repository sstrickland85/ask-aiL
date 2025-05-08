import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ragie API Configuration
RAGIE_API_KEY = os.getenv("RAGIE_API_KEY")
RAGIE_BASE_URL = os.getenv("RAGIE_BASE_URL")

# LLM API Configuration
LLM_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_API_URL = os.getenv("OPENAI_API_URL")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini-2024-07-18")

# Application Configuration
DEBUG = os.getenv("DEBUG", "False").lower() == "true"