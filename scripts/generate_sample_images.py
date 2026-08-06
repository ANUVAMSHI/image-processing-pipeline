import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

SAMPLES_DIR = Path(__file__).parent.parent / "samples"
SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

def create_vehicle_base_image(plate_text="MH12AB1234", brightness=1.0) -> np.ndarray:
    """Generates a synthetic realistic vehicle front image with a license plate."""
    width, height = 800, 600
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Background (Road & Sky)
    img[:250, :] = [210, 180, 140] # Sky/background
    img[250:, :] = [60, 60, 60]   # Asphalt Road

    # Vehicle Body (Sleek Blue Car)
    cv2.rectangle(img, (150, 200), (650, 480), (180, 50, 20), -1) # Blue body
    cv2.rectangle(img, (220, 220), (580, 320), (220, 220, 220), -1) # Windshield

    # Headlights
    cv2.circle(img, (200, 360), 30, (240, 240, 240), -1)
    cv2.circle(img, (600, 360), 30, (240, 240, 240), -1)

    # License Plate Box (White box with Black Border)
    cv2.rectangle(img, (300, 420), (500, 470), (255, 255, 255), -1)
    cv2.rectangle(img, (300, 420), (500, 470), (0, 0, 0), 3)

    # Draw License Plate Text
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except Exception:
        font = ImageFont.load_default()

    draw.text((315, 430), plate_text, fill=(0, 0, 0), font=font)

    bgr_out = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    if brightness != 1.0:
        bgr_out = np.clip(bgr_out * brightness, 0, 255).astype(np.uint8)

    return bgr_out

def generate_samples():
    print("Generating sample test images for evaluation...")

    # 1. Clear Vehicle Image with Valid Plate
    clear_img = create_vehicle_base_image("MH12AB1234", brightness=1.0)
    clear_path = SAMPLES_DIR / "sample_clear_vehicle.jpg"
    cv2.imwrite(str(clear_path), clear_img)

    # 2. Blurry Vehicle Image (Gaussian Blur)
    blurry_img = cv2.GaussianBlur(clear_img, (35, 35), 0)
    blurry_path = SAMPLES_DIR / "sample_blurry_vehicle.jpg"
    cv2.imwrite(str(blurry_path), blurry_img)

    # 3. Low Light Vehicle Image
    dark_img = create_vehicle_base_image("KA05MB9999", brightness=0.18)
    dark_path = SAMPLES_DIR / "sample_low_light_vehicle.jpg"
    cv2.imwrite(str(dark_path), dark_img)

    # 4. Duplicate Image (Identical to clear image)
    dup_path = SAMPLES_DIR / "sample_duplicate_vehicle.jpg"
    cv2.imwrite(str(dup_path), clear_img)

    # 5. Screenshot Mobile Aspect Ratio PNG
    screenshot_pil = Image.new("RGB", (1080, 2340), color=(30, 30, 30))
    screenshot_path = SAMPLES_DIR / "sample_screenshot.png"
    screenshot_pil.save(screenshot_path)

    print(f"[SUCCESS] Generated sample images in {SAMPLES_DIR}:")
    for f in SAMPLES_DIR.iterdir():
        print(f"  - {f.name} ({f.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_samples()
