import os
from pathlib import Path
from dotenv import load_dotenv

# ==========================================================
# Load Environment Variables
# ==========================================================

from dotenv import load_dotenv
from pathlib import Path

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHROMA_DB = os.path.join(BASE_DIR, "..", "chroma_db")

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# ==========================================================
# Project Paths
# ==========================================================

APP_DIR = BASE_DIR / "app"

ML_DIR = APP_DIR / "ml"

RAG_DIR = APP_DIR / "rag"

CACHE_DIR = APP_DIR / "cache"

LOG_DIR = BASE_DIR / "logs"

HISTORY_DIR = BASE_DIR / "history"

KNOWLEDGE_BASE = BASE_DIR / "knowledge_base"

CHROMA_DB = BASE_DIR / "chroma_db"

# ==========================================================
# Create Directories
# ==========================================================

LOG_DIR.mkdir(exist_ok=True)

HISTORY_DIR.mkdir(exist_ok=True)

CHROMA_DB.mkdir(exist_ok=True)

# ==========================================================
# Model Paths
# ==========================================================

MODEL_PATH = ML_DIR / "spam_model.pkl"

VECTORIZER_PATH = ML_DIR / "vectorizer.pkl"

METRICS_PATH = ML_DIR / "metrics.json"

# ==========================================================
# API Keys
# ==========================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================================
# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================================================
# ChromaDB
# ==========================================================

CHROMA_COLLECTION = "email_knowledge"

SEMANTIC_CACHE_COLLECTION = "semantic_cache"

# ==========================================================
# Similarity Threshold
# ==========================================================

CACHE_THRESHOLD = 0.90

TOP_K = 5

# ==========================================================
# FastAPI
# ==========================================================

APP_NAME = "Intelligent Email Automation API"

APP_VERSION = "1.0.0"

DEBUG = True