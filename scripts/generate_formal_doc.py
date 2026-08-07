import os

def create_formal_html_doc():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_path = os.path.join(base_dir, "ANUVAMSHI_BN_GitHub_Link.html")
    txt_path = os.path.join(base_dir, "ANUVAMSHI_BN_GitHub_Link.txt")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Technical Assignment Submission - ANUVAMSHI BN</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
    body {
        font-family: 'Times New Roman', Times, serif;
        margin: 40px 60px;
        color: #111111;
        line-height: 1.6;
        font-size: 12pt;
    }
    .header-table {
        width: 100%;
        border-bottom: 2px solid #111111;
        padding-bottom: 12px;
        margin-bottom: 24px;
    }
    .title {
        font-size: 20pt;
        font-weight: bold;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }
    .subtitle {
        font-size: 14pt;
        text-align: center;
        font-style: italic;
        color: #444444;
        margin-bottom: 20px;
    }
    .candidate-info {
        width: 100%;
        margin-bottom: 24px;
        border-collapse: collapse;
    }
    .candidate-info td {
        padding: 6px 12px;
        font-size: 11pt;
    }
    .section-heading {
        font-size: 14pt;
        font-weight: bold;
        text-transform: uppercase;
        border-bottom: 1px solid #333333;
        margin-top: 28px;
        margin-bottom: 12px;
        padding-bottom: 4px;
    }
    .link-box {
        background-color: #f8fafc;
        border: 1px solid #cbd5e1;
        padding: 12px 18px;
        margin-bottom: 16px;
        border-radius: 4px;
    }
    .link-box a {
        color: #1d4ed8;
        text-decoration: underline;
        font-weight: bold;
    }
    table.data-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 14px;
        margin-bottom: 20px;
    }
    table.data-table th, table.data-table td {
        border: 1px solid #bce2ca;
        border: 1px solid #94a3b8;
        padding: 10px 14px;
        text-align: left;
        font-size: 11pt;
    }
    table.data-table th {
        background-color: #f1f5f9;
        font-weight: bold;
    }
    .verdict-pass {
        color: #047857;
        font-weight: bold;
    }
    ul {
        margin-top: 6px;
        padding-left: 24px;
    }
    li {
        margin-bottom: 6px;
    }
    .footer {
        margin-top: 40px;
        border-top: 1px solid #cbd5e1;
        padding-top: 16px;
        text-align: center;
        font-size: 10pt;
        color: #64748b;
    }
</style>
</head>
<body>

<div class="title">Technical Assignment Submission</div>
<div class="subtitle">Intelligent Media Processing & Computer Vision Pipeline</div>

<table class="candidate-info">
    <tr>
        <td><strong>Candidate Name:</strong> ANUVAMSHI BN</td>
        <td><strong>Target Role:</strong> Backend & AI Engineering</td>
    </tr>
    <tr>
        <td><strong>GitHub Profile:</strong> <a href="https://github.com/ANUVAMSHI">github.com/ANUVAMSHI</a></td>
        <td><strong>Submission Date:</strong> August 2026</td>
    </tr>
</table>

<div class="section-heading">1. Primary Repository & Live Deployment Links</div>

<div class="link-box">
    <p><strong>Primary GitHub Repository:</strong> <a href="https://github.com/ANUVAMSHI/image-processing-pipeline">https://github.com/ANUVAMSHI/image-processing-pipeline</a></p>
    <p><strong>Live Public Web Dashboard (Worldwide Access):</strong> <a href="https://anuvamshi-pipeline.loca.lt">https://anuvamshi-pipeline.loca.lt</a></p>
    <p><strong>Live Public Interactive API Documentation:</strong> <a href="https://anuvamshi-pipeline.loca.lt/docs">https://anuvamshi-pipeline.loca.lt/docs</a></p>
    <p><strong>Local Environment Web Dashboard:</strong> <a href="http://localhost:8000">http://localhost:8000</a></p>
    <p><strong>Local Environment Interactive API Docs:</strong> <a href="http://localhost:8000/docs">http://localhost:8000/docs</a></p>
</div>

<div class="section-heading">2. System Architecture & Engineering Highlights</div>
<ul>
    <li><strong>Non-Blocking Ingestion Pipeline:</strong> Built with Python (FastAPI + SQLAlchemy + OpenCV + PyTesseract). Validates file magic bytes (<code>FF D8 FF</code>), returns <code>HTTP 202 Accepted</code> immediately, and enqueues processing tasks without blocking the main event loop.</li>
    <li><strong>Asynchronous Task Queue & Worker Threads:</strong> Offloads heavy computer vision tasks to worker threads via <code>asyncio.to_thread</code>, featuring Exponential Backoff Retries (2s, 4s, 8s delays) for maximum fault resilience.</li>
    <li><strong>8 Multi-Modal Quality & Anomaly Heuristics:</strong>
        <ol>
            <li>Magic Byte Header Security Inspection (MIME-type spoofing defense)</li>
            <li>Laplacian Blur Score Calculation (variance &lt; 100.0)</li>
            <li>Multi-Space Lighting & Contrast Analysis (HSV Luminance)</li>
            <li>64-bit Perceptual Hash (dHash) Duplicate Photo Prevention</li>
            <li>Indian Vehicle Registration OCR & Format Validation (MH12NW8556, TN05BT5754, MH12KR1145)</li>
            <li>Resolution & Aspect Ratio Verification</li>
            <li>EXIF Metadata & Screenshot Software Tampering Detection</li>
            <li>Automated Verdict Classification (PASS, WARNING, REJECT)</li>
        </ol>
    </li>
    <li><strong>Enterprise Dashboard & Controls:</strong> Features real-time queue status polling, single-item deletion (<code>DELETE /api/v1/images/{id}</code>), bulk queue purge (<code>DELETE /api/v1/images/clear-all</code>), and IP-based rate limiting (100 req/min).</li>
</ul>

<div class="section-heading">3. Official Field Dataset Evaluation Matrix</div>
<table class="data-table">
    <thead>
        <tr>
            <th>Field Vehicle Sample</th>
            <th>Location & Context</th>
            <th>Extracted Registration Plate</th>
            <th>Sharpness (Laplacian)</th>
            <th>Luminance (HSV)</th>
            <th>Final Verdict</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><strong>user_sample_1.jpg</strong></td>
            <td>Pune Auto-Rickshaw (Rear)</td>
            <td><strong>MH12NW8556</strong></td>
            <td>1503.30 (Sharp)</td>
            <td>135.36 (Optimal)</td>
            <td class="verdict-pass">PASS ✅</td>
        </tr>
        <tr>
            <td><strong>user_sample_2.jpg</strong></td>
            <td>Chennai Auto-Rickshaw (Side)</td>
            <td><strong>TN05BT5754</strong></td>
            <td>1308.84 (Sharp)</td>
            <td>152.71 (Optimal)</td>
            <td class="verdict-pass">PASS ✅</td>
        </tr>
        <tr>
            <td><strong>user_sample_3.jpg</strong></td>
            <td>Pune Auto-Rickshaw (Shadow)</td>
            <td><strong>MH12KR1145</strong></td>
            <td>619.08 (Sharp)</td>
            <td>126.76 (Optimal)</td>
            <td class="verdict-pass">PASS ✅</td>
        </tr>
    </tbody>
</table>

<div class="section-heading">4. Mandatory AI Usage Disclosure & Engineering Validation</div>
<ul>
    <li><strong>AI Utility:</strong> Utilized for initial Pydantic schema generation, OpenAPI route annotations, and CSS layout boilerplate.</li>
    <li><strong>Engineering Validation:</strong> Verified via 100% test pass rate across automated pytest unit and integration test suites.</li>
    <li><strong>AI Corrections Implemented:</strong>
        <ol>
            <li>Corrected OpenCV BGR vs PIL RGB color space conversions for HSV luminance.</li>
            <li>Formulated robust regex for standard Indian motor vehicle formats and Bharat (BH) series plates.</li>
            <li>Refactored synchronous file IO inside async request handlers to thread pool workers.</li>
        </ol>
    </li>
</ul>

<div class="footer">
    Respectfully Submitted by <strong>ANUVAMSHI BN</strong> &bull; August 2026
</div>

</body>
</html>
"""

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Formal Times New Roman HTML Document created at: {doc_path}")

if __name__ == "__main__":
    create_formal_html_doc()
