from datetime import datetime
import enum
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class ProcessingStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Verdict(str, enum.Enum):
    PASS = "PASS"
    WARNING = "WARNING"
    REJECT = "REJECT"

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    status = Column(String, default=ProcessingStatus.PENDING.value, index=True)
    phash = Column(String, nullable=True, index=True)
    retry_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)

    analysis_result = relationship("AnalysisResultRecord", back_populates="image", uselist=False, cascade="all, delete-orphan")

class AnalysisResultRecord(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    image_id = Column(String, ForeignKey("images.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)

    is_blurry = Column(Boolean, default=False)
    blur_score = Column(Float, default=0.0)

    is_low_light = Column(Boolean, default=False)
    brightness_score = Column(Float, default=0.0)

    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(String, nullable=True)

    detected_plate = Column(String, nullable=True)
    is_valid_plate = Column(Boolean, default=False)

    is_screenshot = Column(Boolean, default=False)
    width = Column(Integer, default=0)
    height = Column(Integer, default=0)

    overall_verdict = Column(String, default=Verdict.PASS.value)
    flagged_issues = Column(JSON, default=list)
    raw_metadata = Column(JSON, default=dict)

    image = relationship("ImageRecord", back_populates="analysis_result")
