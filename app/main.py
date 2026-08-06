import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Dict, List

from app.config import settings
from app.db.database import engine, Base
from app.api.routes import router as image_router, analytics_router
from app.services.queue import task_queue

# Create DB Tables if not exist
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start Background Worker Queue
    await task_queue.start()
    yield
    # Shutdown: Stop Background Workers
    await task_queue.stop()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Intelligent Media Processing Pipeline - Asynchronous quality analysis & anomaly detection engine for vehicle media.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting Middleware (100 requests per minute per IP)
client_request_history: Dict[str, List[float]] = {}
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_SEC = 60.0

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # Skip rate limiting for static assets
    if request.url.path.startswith("/styles.css") or request.url.path.startswith("/app.js") or request.url.path == "/":
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"
    now = time.time()

    # Clean old requests outside window
    timestamps = [t for t in client_request_history.get(client_ip, []) if now - t < RATE_LIMIT_WINDOW_SEC]
    
    if len(timestamps) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded ({RATE_LIMIT_REQUESTS} req/min). Please wait before sending more requests."
        )

    timestamps.append(now)
    client_request_history[client_ip] = timestamps

    response = await call_next(request)
    return response

# Include Routers
app.include_router(image_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)

# Serve Static Dashboard UI
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
