import asyncio
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.image import ImageRecord, ProcessingStatus
from app.services.analyzer import ImageAnalyzer
from app.config import settings

logger = logging.getLogger("media_pipeline.queue")
logging.basicConfig(level=logging.INFO)

class TaskQueueEngine:
    """
    Asynchronous queue and worker manager supporting:
    - Non-blocking task submission
    - In-memory async queue with database persistence
    - Concurrency control via async workers
    - Exponential backoff retries and error state handling
    """

    def __init__(self, concurrency: int = settings.WORKER_CONCURRENCY):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.concurrency: int = concurrency
        self.worker_tasks: list[asyncio.Task] = []
        self._is_running: bool = False

    async def start(self):
        """Starts worker tasks in the background."""
        if self._is_running:
            return
        self._is_running = True
        for i in range(self.concurrency):
            task = asyncio.create_task(self._worker_loop(worker_id=i + 1))
            self.worker_tasks.append(task)
        logger.info(f"TaskQueueEngine started with {self.concurrency} worker tasks.")

    async def stop(self):
        """Gracefully shuts down worker tasks."""
        if not self._is_running:
            return
        self._is_running = False
        for _ in self.worker_tasks:
            await self.queue.put(None)  # Sentinel to stop worker loops
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        logger.info("TaskQueueEngine gracefully stopped.")

    async def enqueue(self, image_id: str):
        """Enqueues an image ID for asynchronous background processing."""
        await self.queue.put(image_id)
        logger.info(f"Enqueued image job: {image_id}")

    async def _worker_loop(self, worker_id: int):
        """Worker loop picking jobs off the queue and executing image analysis."""
        logger.info(f"Worker-{worker_id} ready for processing.")
        while self._is_running:
            image_id = await self.queue.get()
            if image_id is None:
                self.queue.task_done()
                break

            try:
                await self._process_job(image_id, worker_id)
            except Exception as e:
                logger.error(f"Worker-{worker_id} unexpected error processing {image_id}: {str(e)}")
            finally:
                self.queue.task_done()

    async def _process_job(self, image_id: str, worker_id: int):
        """Executes job with retry logic and database status transitions."""
        db: Session = SessionLocal()
        try:
            image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
            if not image_rec:
                logger.warning(f"Worker-{worker_id}: Image ID {image_id} not found in DB.")
                return

            # Transition state to 'processing'
            image_rec.status = ProcessingStatus.PROCESSING.value
            db.commit()
            logger.info(f"Worker-{worker_id}: Processing image {image_id}")

            # Run Analysis in threadpool so CPU-bound OpenCV / OCR doesn't block async event loop
            try:
                analysis_rec = await asyncio.to_thread(ImageAnalyzer.analyze_image, db, image_rec)

                # Save analysis result & mark completed
                db.add(analysis_rec)
                image_rec.status = ProcessingStatus.COMPLETED.value
                image_rec.processed_at = datetime.utcnow()
                image_rec.error_message = None
                db.commit()
                logger.info(f"Worker-{worker_id}: Successfully completed image {image_id} (Verdict: {analysis_rec.overall_verdict})")

            except Exception as analysis_err:
                db.rollback()
                image_rec = db.query(ImageRecord).filter(ImageRecord.id == image_id).first()
                if not image_rec:
                    return

                image_rec.retry_count += 1
                if image_rec.retry_count <= settings.MAX_RETRIES:
                    backoff_delay = 2 ** image_rec.retry_count
                    logger.warning(
                        f"Worker-{worker_id}: Analysis failed for {image_id} (Attempt {image_rec.retry_count}/{settings.MAX_RETRIES}). "
                        f"Retrying in {backoff_delay}s. Error: {str(analysis_err)}"
                    )
                    image_rec.status = ProcessingStatus.PENDING.value
                    image_rec.error_message = f"Retry {image_rec.retry_count}: {str(analysis_err)}"
                    db.commit()

                    await asyncio.sleep(backoff_delay)
                    await self.enqueue(image_id)
                else:
                    logger.error(f"Worker-{worker_id}: Max retries reached for image {image_id}. Marking FAILED.")
                    image_rec.status = ProcessingStatus.FAILED.value
                    image_rec.error_message = f"Failed after {settings.MAX_RETRIES} attempts: {str(analysis_err)}"
                    image_rec.processed_at = datetime.utcnow()
                    db.commit()

        finally:
            db.close()

# Global Singleton Queue Instance
task_queue = TaskQueueEngine()
