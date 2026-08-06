import pytest
import io
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def create_dummy_jpeg():
    file = io.BytesIO()
    image = Image.new('RGB', size=(800, 600), color=(150, 150, 150))
    image.save(file, 'jpeg')
    file.seek(0)
    return file

def test_upload_and_status_flow():
    dummy_file = create_dummy_jpeg()
    
    # 1. Upload API
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test_vehicle.jpg", dummy_file, "image/jpeg")}
    )
    assert response.status_code == 202
    data = response.json()
    assert "image_id" in data
    assert data["status"] == "pending"

    image_id = data["image_id"]

    # 2. Status API
    status_res = client.get(f"/api/v1/images/{image_id}/status")
    assert status_res.status_code == 200
    status_data = status_res.json()
    assert status_data["image_id"] == image_id
    assert status_data["status"] in ["pending", "processing", "completed"]

def test_invalid_mime_type_upload():
    response = client.post(
        "/api/v1/images/upload",
        files={"file": ("test.txt", io.BytesIO(b"hello text"), "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]

def test_list_images():
    response = client.get("/api/v1/images")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_summary():
    response = client.get("/api/v1/analytics/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_images" in data
    assert "common_flagged_issues" in data
