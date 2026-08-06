from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict

class ImageUploadResponse(BaseModel):
    image_id: str
    filename: str
    status: str
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ImageStatusResponse(BaseModel):
    image_id: str
    status: str
    retry_count: int
    error_message: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class AnalysisResultResponse(BaseModel):
    image_id: str
    is_blurry: bool
    blur_score: float
    is_low_light: bool
    brightness_score: float
    is_duplicate: bool
    duplicate_of_id: Optional[str] = None
    detected_plate: Optional[str] = None
    is_valid_plate: bool
    is_screenshot: bool
    width: int
    height: int
    overall_verdict: str
    flagged_issues: List[str]
    raw_metadata: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)

class ImageDetailResponse(BaseModel):
    id: str
    filename: str
    file_size: int
    mime_type: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    analysis: Optional[AnalysisResultResponse] = None

    model_config = ConfigDict(from_attributes=True)

class AnalyticsSummaryResponse(BaseModel):
    total_images: int
    pending_count: int
    processing_count: int
    completed_count: int
    failed_count: int
    pass_count: int
    warning_count: int
    reject_count: int
    common_flagged_issues: Dict[str, int]
