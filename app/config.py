import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings:
    PROJECT_NAME: str = "Intelligent Media Processing Pipeline"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/media_pipeline.db")

    # Uploads
    UPLOAD_DIR: Path = Path(os.getenv("UPLOAD_DIR", BASE_DIR / "uploads"))
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", 10))
    ALLOWED_MIME_TYPES: list = ["image/jpeg", "image/png", "image/webp"]

    # Worker & Queue
    WORKER_CONCURRENCY: int = int(os.getenv("WORKER_CONCURRENCY", 2))
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", 3))

    # Thresholds for Image Heuristics
    BLUR_THRESHOLD: float = float(os.getenv("BLUR_THRESHOLD", 100.0))
    LOW_LIGHT_THRESHOLD: float = float(os.getenv("LOW_LIGHT_THRESHOLD", 45.0))
    OVEREXPOSURE_THRESHOLD: float = float(os.getenv("OVEREXPOSURE_THRESHOLD", 215.0))
    DUPLICATE_HAMMING_THRESHOLD: int = int(os.getenv("DUPLICATE_HAMMING_THRESHOLD", 4))

settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
