import asyncio
import httpx
from pathlib import Path
import sys

# Ensure sample images exist
from generate_sample_images import generate_samples, SAMPLES_DIR

API_URL = "http://localhost:8000/api/v1/images/upload"

async def seed_data():
    generate_samples()
    print("\nSeeding field sample images & synthetic data into running FastAPI application...")

    sample_files = list(SAMPLES_DIR.glob("*.*"))
    if not sample_files:
        print("No sample files found.")
        return

    # Prioritize user provided field sample images first
    sample_files.sort(key=lambda x: 0 if "user_sample" in x.name else 1)

    async with httpx.AsyncClient(timeout=15.0) as client:
        for file_path in sample_files:
            mime_type = "image/png" if file_path.suffix == ".png" else "image/jpeg"
            print(f"Uploading {file_path.name} ({mime_type})...")
            
            with open(file_path, "rb") as f:
                files = {"file": (file_path.name, f, mime_type)}
                try:
                    response = await client.post(API_URL, files=files)
                    if response.status_code == 202:
                        res_json = response.json()
                        print(f"  [SUCCESS] Queued! Image ID: {res_json['image_id']} (Status: {res_json['status']})")
                    else:
                        print(f"  [FAILED] Upload Error ({response.status_code}): {response.text}")
                except Exception as e:
                    print(f"  [ERROR] Connection error (Is FastAPI server running on http://localhost:8000?): {str(e)}")

    print("\n[COMPLETED] Seeding completed! Access dashboard UI at http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(seed_data())
