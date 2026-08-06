import uuid
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.config import settings
from app.db.database import get_db
from app.models.image import ImageRecord, AnalysisResultRecord, ProcessingStatus, Verdict
from app.schemas.image import (
    ImageUploadResponse,
    ImageStatusResponse,
    AnalysisResultResponse,
    ImageDetailResponse,
    AnalyticsSummaryResponse,
)
from app.services.queue import task_queue

router = APIRouter(prefix="/images", tags=["Media Processing"])
analytics_router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.post("/upload", response_model=ImageUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Accepts vehicle image upload from the field, saves metadata,
    and enqueues background processing task immediately.
    """
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{file.content_type}'. Allowed types: {settings.ALLOWED_MIME_TYPES}"
        )

    contents = await file.read()
    file_size = len(contents)
    max_size_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024

    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE_MB}MB."
        )

    image_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix or ".jpg"
    saved_filename = f"{image_id}{file_extension}"
    file_save_path = settings.UPLOAD_DIR / saved_filename

    with open(file_save_path, "wb") as f:
        f.write(contents)

    image_rec = ImageRecord(
        id=image_id,
        filename=file.filename,
        file_path=str(file_save_path),
        file_size=file_size,
        mime_type=file.content_type,
        status=ProcessingStatus.PENDING.value
    )
    db.add(image_rec)
    db.commit()
    db.refresh(image_rec)

    await task_queue.enqueue(image_id)

    return ImageUploadResponse(
        image_id=image_rec.id,
        filename=image_rec.filename,
        status=image_rec.status,
        message="Image successfully uploaded and queued for processing.",
        created_at=image_rec.created_at
    )

@router.post("/process-sample/{sample_name}", response_model=ImageUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def process_sample_image(sample_name: str, db: Session = Depends(get_db)):
    """Processes a sample image from the server samples directory by name."""
    samples_dir = Path(__file__).parent.parent.parent / "samples"
    sample_file = samples_dir / sample_name

    if not sample_file.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sample '{sample_name}' not found.")

    with open(sample_file, "rb") as f:
        contents = f.read()

    image_id = str(uuid.uuid4())
    mime_type = "image/png" if sample_file.suffix == ".png" else "image/jpeg"
    saved_filename = f"{image_id}{sample_file.suffix}"
    file_save_path = settings.UPLOAD_DIR / saved_filename

    with open(file_save_path, "wb") as f:
        f.write(contents)

    image_rec = ImageRecord(
        id=image_id,
        filename=sample_name,
        file_path=str(file_save_path),
        file_size=len(contents),
        mime_type=mime_type,
        status=ProcessingStatus.PENDING.value
    )
    db.add(image_rec)
    db.commit()
    db.refresh(image_rec)

    await task_queue.enqueue(image_id)

    return ImageUploadResponse(
        image_id=image_rec.id,
        filename=image_rec.filename,
        status=image_rec.status,
        message="Sample image queued for processing.",
        created_at=image_rec.created_at
    )

@router.delete("/clear-all", status_code=status.HTTP_200_OK)
def clear_all_queue(db: Session = Depends(get_db)):
    """Deletes all processing queue records and analysis results from the database."""
    db.query(AnalysisResultRecord).delete()
    db.query(ImageRecord).delete()
    db.commit()
    return {"message": "Processing queue and all database records cleared successfully."}

@router.delete("/{image_id}", status_code=status.HTTP_200_OK)
def delete_single_image(image_id: str, db: Session = Depends(get_db)):
    """Deletes an individual image record, its analysis result, and file from disk."""
    image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
    if not image_rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image record not found.")

    # Delete physical file from disk if exists
    if image_rec.file_path and os.path.exists(image_rec.file_path):
        try:
            os.remove(image_rec.file_path)
        except Exception:
            pass

    # Delete DB records
    if image_rec.analysis_result:
        db.delete(image_rec.analysis_result)
    db.delete(image_rec)
    db.commit()

    return {"message": f"Image '{image_id}' deleted successfully."}

@router.get("/{image_id}/status", response_model=ImageStatusResponse)
def get_image_status(image_id: str, db: Session = Depends(get_db)):
    """Fetches real-time processing status for a given image ID."""
    image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
    if not image_rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return ImageStatusResponse(
        image_id=image_rec.id,
        status=image_rec.status,
        retry_count=image_rec.retry_count,
        error_message=image_rec.error_message,
        created_at=image_rec.created_at,
        processed_at=image_rec.processed_at
    )

@router.get("/{image_id}/results", response_model=AnalysisResultResponse)
def get_image_results(image_id: str, db: Session = Depends(get_db)):
    """Fetches detailed analysis results, quality heuristics, and detected issues."""
    image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
    if not image_rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    if image_rec.status == ProcessingStatus.PENDING.value or image_rec.status == ProcessingStatus.PROCESSING.value:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=f"Image processing is still in state '{image_rec.status}'. Please poll status endpoint."
        )

    if image_rec.status == ProcessingStatus.FAILED.value:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Processing failed: {image_rec.error_message}"
        )

    if not image_rec.analysis_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis results unavailable.")

    return image_rec.analysis_result

@router.get("/{image_id}/file")
def get_image_file(image_id: str, db: Session = Depends(get_db)):
    """Streams the raw image file for rendering in frontend UI."""
    image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
    if not image_rec or not Path(image_rec.file_path).exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image file not found")

    return FileResponse(image_rec.file_path, media_type=image_rec.mime_type)

@router.get("", response_model=List[ImageDetailResponse])
def list_images(
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Returns paginated list of uploaded images with optional status filter."""
    query = db.query(ImageRecord)
    if status_filter:
        query = query.filter(ImageRecord.status == status_filter)

    images = query.order_by(ImageRecord.created_at.desc()).offset(offset).limit(limit).all()
    
    results = []
    for img in images:
        analysis_data = None
        if img.analysis_result:
            analysis_data = AnalysisResultResponse.model_validate(img.analysis_result)
        
        results.append(ImageDetailResponse(
            id=img.id,
            filename=img.filename,
            file_size=img.file_size,
            mime_type=img.mime_type,
            status=img.status,
            created_at=img.created_at,
            processed_at=img.processed_at,
            error_message=img.error_message,
            analysis=analysis_data
        ))
    return results

@analytics_router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(db: Session = Depends(get_db)):
    """Aggregates system analytics, pass rates, and common flagged issue statistics."""
    total_images = db.query(ImageRecord).count()
    pending_count = db.query(ImageRecord).filter(ImageRecord.status == ProcessingStatus.PENDING.value).count()
    processing_count = db.query(ImageRecord).filter(ImageRecord.status == ProcessingStatus.PROCESSING.value).count()
    completed_count = db.query(ImageRecord).filter(ImageRecord.status == ProcessingStatus.COMPLETED.value).count()
    failed_count = db.query(ImageRecord).filter(ImageRecord.status == ProcessingStatus.FAILED.value).count()

    pass_count = db.query(AnalysisResultRecord).filter(AnalysisResultRecord.overall_verdict == Verdict.PASS.value).count()
    warning_count = db.query(AnalysisResultRecord).filter(AnalysisResultRecord.overall_verdict == Verdict.WARNING.value).count()
    reject_count = db.query(AnalysisResultRecord).filter(AnalysisResultRecord.overall_verdict == Verdict.REJECT.value).count()

    all_results = db.query(AnalysisResultRecord.flagged_issues).all()
    common_issues: dict[str, int] = {}
    for res in all_results:
        issues = res[0] or []
        for issue in issues:
            category = issue.split("(")[0].strip() if "(" in issue else issue
            common_issues[category] = common_issues.get(category, 0) + 1

    return AnalyticsSummaryResponse(
        total_images=total_images,
        pending_count=pending_count,
        processing_count=processing_count,
        completed_count=completed_count,
        failed_count=failed_count,
        pass_count=pass_count,
        warning_count=warning_count,
        reject_count=reject_count,
        common_flagged_issues=common_issues
    )
