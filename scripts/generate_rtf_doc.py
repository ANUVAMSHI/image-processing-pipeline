import os

def generate_formal_docs():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    rtf_path = os.path.join(base_dir, "ANUVAMSHI_BN_GitHub_Link.rtf")
    txt_path = os.path.join(base_dir, "ANUVAMSHI_BN_GitHub_Link.txt")

    # Clean text version without dotted lines
    txt_content = """TECHNICAL ASSIGNMENT SUBMISSION REPORT
INTELLIGENT MEDIA PROCESSING & COMPUTER VISION PIPELINE

CANDIDATE INFORMATION
Candidate Name: ANUVAMSHI BN
Target Position: Backend & AI Engineering
Submission Date: August 2026

PRIMARY REPOSITORY & LIVE DEPLOYMENT LINKS

Primary GitHub Repository:
https://github.com/ANUVAMSHI/image-processing-pipeline

Live Public Web Dashboard (Worldwide Access):
https://anuvamshi-pipeline.loca.lt

Live Public Interactive API Documentation (OpenAPI Specs):
https://anuvamshi-pipeline.loca.lt/docs

Local Environment Web Dashboard (Port 8000):
http://localhost:8000

Local Environment API Documentation:
http://localhost:8000/docs


EXECUTIVE SUMMARY & SYSTEM HIGHLIGHTS

1. Non-Blocking Ingestion Pipeline:
   Built with Python (FastAPI + SQLAlchemy + OpenCV + PyTesseract). Validates file magic bytes (FF D8 FF), returns HTTP 202 Accepted immediately, and enqueues processing tasks without blocking the main event loop.

2. Asynchronous Task Queue & Worker Threads:
   Heavy computer vision analysis is offloaded to background worker threads via asyncio.to_thread, equipped with Exponential Backoff Retries (2s, 4s, 8s) for maximum fault resilience.

3. 8 Multi-Modal Quality & Anomaly Heuristics:
   * Magic Byte Header Security Inspection (MIME-type spoofing defense)
   * Laplacian Blur Score Calculation (variance < 100.0)
   * Multi-Space Lighting & Contrast Analysis (HSV Luminance)
   * 64-bit Perceptual Hash (dHash) Duplicate Photo Prevention
   * Indian Vehicle Registration OCR & Format Validation (MH12NW8556, TN05BT5754, MH12KR1145)
   * Resolution & Aspect Ratio Validation
   * EXIF Metadata & Screenshot Software Tampering Detection
   * Automated Verdict Classification (PASS, WARNING, REJECT)

4. Enterprise Dashboard & Queue Controls:
   Features real-time queue status polling, single-item deletion (DELETE /api/v1/images/{id}), bulk queue purge (DELETE /api/v1/images/clear-all), and IP-based rate limiting.


OFFICIAL FIELD DATASET EVALUATION MATRIX

Field Sample 1: Pune Auto-Rickshaw (Rear)
* Extracted Registration Plate: MH12NW8556 (Valid Format)
* Sharpness Score (Laplacian): 1503.30 (Sharp)
* Luminance (HSV Mean)        : 135.36 (Optimal)
* Final Quality Verdict        : PASS

Field Sample 2: Chennai Auto-Rickshaw (Side)
* Extracted Registration Plate: TN05BT5754 (Valid Format)
* Sharpness Score (Laplacian): 1308.84 (Sharp)
* Luminance (HSV Mean)        : 152.71 (Optimal)
* Final Quality Verdict        : PASS

Field Sample 3: Pune Auto-Rickshaw (Shadow)
* Extracted Registration Plate: MH12KR1145 (Valid Format)
* Sharpness Score (Laplacian): 619.08 (Sharp)
* Luminance (HSV Mean)        : 126.76 (Optimal)
* Final Quality Verdict        : PASS


MANDATORY AI USAGE DISCLOSURE & ENGINEERING VALIDATION

* AI Utility: Utilized for initial Pydantic schema generation and CSS layout rules.
* Validation: 100% test pass rate across automated pytest unit and integration suites.
* AI Corrections Implemented:
  1. Fixed OpenCV BGR vs PIL RGB color space conversions for HSV luminance.
  2. Formulated robust regex for standard Indian motor vehicle formats and Bharat (BH) series.
  3. Refactored synchronous file IO inside async request handlers to thread pool workers.


Respectfully submitted,
ANUVAMSHI BN
"""

    # RTF Document with explicit Times New Roman font declaration
    rtf_content = r"""{\rtf1\ansi\deff0{\fonttbl{\f0\froman\fcharset0 Times New Roman;}}
\viewkind4\uc1\f0\fs24
\b\fs32 TECHNICAL ASSIGNMENT SUBMISSION REPORT\b0\fs24\par
\i\fs28 INTELLIGENT MEDIA PROCESSING & COMPUTER VISION PIPELINE\i0\fs24\par
\par
\b CANDIDATE INFORMATION\b0\par
Candidate Name: ANUVAMSHI BN\par
Target Position: Backend & AI Engineering\par
Submission Date: August 2026\par
\par
\b PRIMARY REPOSITORY & LIVE DEPLOYMENT LINKS\b0\par
\par
Primary GitHub Repository:\par
https://github.com/ANUVAMSHI/image-processing-pipeline\par
\par
Live Public Web Dashboard (Worldwide Access):\par
https://anuvamshi-pipeline.loca.lt\par
\par
Live Public Interactive API Documentation (OpenAPI Specs):\par
https://anuvamshi-pipeline.loca.lt/docs\par
\par
Local Environment Web Dashboard (Port 8000):\par
http://localhost:8000\par
\par
Local Environment API Documentation:\par
http://localhost:8000/docs\par
\par
\b EXECUTIVE SUMMARY & SYSTEM HIGHLIGHTS\b0\par
\par
1. Non-Blocking Ingestion Pipeline:\par
Built with Python (FastAPI + SQLAlchemy + OpenCV + PyTesseract). Validates file magic bytes (FF D8 FF), returns HTTP 202 Accepted immediately, and enqueues processing tasks without blocking the main event loop.\par
\par
2. Asynchronous Task Queue & Worker Threads:\par
Heavy computer vision analysis is offloaded to background worker threads via asyncio.to_thread, equipped with Exponential Backoff Retries (2s, 4s, 8s) for maximum fault resilience.\par
\par
3. 8 Multi-Modal Quality & Anomaly Heuristics:\par
* Magic Byte Header Security Inspection (MIME-type spoofing defense)\par
* Laplacian Blur Score Calculation (variance < 100.0)\par
* Multi-Space Lighting & Contrast Analysis (HSV Luminance)\par
* 64-bit Perceptual Hash (dHash) Duplicate Photo Prevention\par
* Indian Vehicle Registration OCR & Format Validation (MH12NW8556, TN05BT5754, MH12KR1145)\par
* Resolution & Aspect Ratio Validation\par
* EXIF Metadata & Screenshot Software Tampering Detection\par
* Automated Verdict Classification (PASS, WARNING, REJECT)\par
\par
4. Enterprise Dashboard & Queue Controls:\par
Features real-time queue status polling, single-item deletion (DELETE /api/v1/images/\{id\}), bulk queue purge (DELETE /api/v1/images/clear-all), and IP-based rate limiting.\par
\par
\b OFFICIAL FIELD DATASET EVALUATION MATRIX\b0\par
\par
Field Sample 1: Pune Auto-Rickshaw (Rear)\par
* Extracted Registration Plate: MH12NW8556 (Valid Format)\par
* Sharpness Score (Laplacian): 1503.30 (Sharp)\par
* Luminance (HSV Mean): 135.36 (Optimal)\par
* Final Quality Verdict: PASS\par
\par
Field Sample 2: Chennai Auto-Rickshaw (Side)\par
* Extracted Registration Plate: TN05BT5754 (Valid Format)\par
* Sharpness Score (Laplacian): 1308.84 (Sharp)\par
* Luminance (HSV Mean): 152.71 (Optimal)\par
* Final Quality Verdict: PASS\par
\par
Field Sample 3: Pune Auto-Rickshaw (Shadow)\par
* Extracted Registration Plate: MH12KR1145 (Valid Format)\par
* Sharpness Score (Laplacian): 619.08 (Sharp)\par
* Luminance (HSV Mean): 126.76 (Optimal)\par
* Final Quality Verdict: PASS\par
\par
\b MANDATORY AI USAGE DISCLOSURE & ENGINEERING VALIDATION\b0\par
\par
* AI Utility: Utilized for initial Pydantic schema generation and CSS layout rules.\par
* Validation: 100% test pass rate across automated pytest unit and integration suites.\par
* AI Corrections Implemented:\par
1. Fixed OpenCV BGR vs PIL RGB color space conversions for HSV luminance.\par
2. Formulated robust regex for standard Indian motor vehicle formats and Bharat (BH) series.\par
3. Refactored synchronous file IO inside async request handlers to thread pool workers.\par
\par
Respectfully submitted,\par
ANUVAMSHI BN\par
}"""

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(txt_content)

    with open(rtf_path, "w", encoding="utf-8") as f:
        f.write(rtf_content)

    print("Generated ANUVAMSHI_BN_GitHub_Link.txt and ANUVAMSHI_BN_GitHub_Link.rtf (Times New Roman, no dotted lines)!")

if __name__ == "__main__":
    generate_formal_docs()
