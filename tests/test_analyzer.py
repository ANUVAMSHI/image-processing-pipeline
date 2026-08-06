import pytest
import numpy as np
import cv2
from pathlib import Path
from app.services.analyzer import ImageAnalyzer, INDIAN_PLATE_PATTERN

def test_blur_detection():
    # Create sharp grid image vs blurred image
    sharp_img = np.zeros((300, 300), dtype=np.uint8)
    cv2.rectangle(sharp_img, (50, 50), (250, 250), 255, 10)
    
    is_blurry_sharp, score_sharp = ImageAnalyzer.detect_blur(sharp_img)
    assert not is_blurry_sharp
    assert score_sharp > 100.0

    blurry_img = cv2.GaussianBlur(sharp_img, (25, 25), 0)
    is_blurry, score_blur = ImageAnalyzer.detect_blur(blurry_img)
    assert is_blurry
    assert score_blur < 100.0

def test_brightness_analysis():
    dark_bgr = np.ones((100, 100, 3), dtype=np.uint8) * 20
    is_low_light, score_dark, is_overexposed = ImageAnalyzer.analyze_brightness(dark_bgr)
    assert is_low_light
    assert not is_overexposed
    assert score_dark < 45.0

    bright_bgr = np.ones((100, 100, 3), dtype=np.uint8) * 240
    is_low_light_b, score_bright, is_overexposed_b = ImageAnalyzer.analyze_brightness(bright_bgr)
    assert not is_low_light_b
    assert is_overexposed_b

def test_indian_plate_regex():
    valid_plates = ["MH12AB1234", "KA05MB9999", "DL1C1234", "TN 01 AA 1111", "22BH1234AA"]
    for plate in valid_plates:
        match = INDIAN_PLATE_PATTERN.search(plate)
        assert match is not None, f"Failed to match valid plate: {plate}"

    invalid_plates = ["123456", "INVALID_PLATE", "XYZ"]
    for plate in invalid_plates:
        match = INDIAN_PLATE_PATTERN.search(plate)
        assert match is None, f"Incorrectly matched invalid plate: {plate}"

def test_dimension_validation():
    is_low_res, is_abnormal = ImageAnalyzer.check_dimensions_and_aspect(300, 400)
    assert is_low_res

    is_low_res_good, is_abnormal_good = ImageAnalyzer.check_dimensions_and_aspect(1080, 1920)
    assert not is_low_res_good
    assert not is_abnormal_good
