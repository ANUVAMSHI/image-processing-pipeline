const API_BASE = '/api/v1';

let selectedFile = null;

// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const previewContainer = document.getElementById('preview-container');
const imagePreview = document.getElementById('image-preview');
const previewFilename = document.getElementById('preview-filename');
const cancelBtn = document.getElementById('cancel-btn');
const uploadBtn = document.getElementById('upload-btn');
const imageList = document.getElementById('image-list');
const statusFilter = document.getElementById('status-filter');
const refreshBtn = document.getElementById('refresh-btn');
const runAllSamplesBtn = document.getElementById('run-all-samples-btn');
const clearQueueBtn = document.getElementById('clear-queue-btn');

const statTotal = document.getElementById('stat-total');
const statPass = document.getElementById('stat-pass');
const statWarning = document.getElementById('stat-warning');
const statReject = document.getElementById('stat-reject');

const detailModal = document.getElementById('detail-modal');
const modalClose = document.getElementById('modal-close');
const modalBodyContent = document.getElementById('modal-body-content');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    dropZone.addEventListener('click', () => fileInput.click());
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    cancelBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetFileInput();
    });

    uploadBtn.addEventListener('click', uploadSelectedImage);
    statusFilter.addEventListener('change', fetchImageList);
    refreshBtn.addEventListener('click', fetchAllData);
    if (runAllSamplesBtn) {
        runAllSamplesBtn.addEventListener('click', runFullTestSuite);
    }
    if (clearQueueBtn) {
        clearQueueBtn.addEventListener('click', clearAllQueueItems);
    }
    modalClose.addEventListener('click', closeModal);

    // Initial Data Fetch & Auto Polling Loop (every 2 seconds)
    fetchAllData();
    setInterval(fetchAllData, 2000);
}

function handleFileSelect(file) {
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
        alert('Unsupported file format. Please select JPEG, PNG, or WEBP.');
        return;
    }
    selectedFile = file;
    previewFilename.textContent = file.name;

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewContainer.classList.remove('hidden');
        dropZone.querySelector('.drop-zone-content').classList.add('hidden');
        uploadBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

function resetFileInput() {
    selectedFile = null;
    fileInput.value = '';
    imagePreview.src = '';
    previewContainer.classList.add('hidden');
    dropZone.querySelector('.drop-zone-content').classList.remove('hidden');
    uploadBtn.disabled = true;
}

async function uploadSelectedImage() {
    if (!selectedFile) return;

    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Uploading & Enqueuing...';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch(`${API_BASE}/images/upload`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Upload failed');
        }

        resetFileInput();
        uploadBtn.textContent = 'Process Image';
        fetchAllData();

    } catch (err) {
        alert(`Upload Error: ${err.message}`);
        uploadBtn.disabled = false;
        uploadBtn.textContent = 'Process Image';
    }
}

async function uploadSampleByName(sampleName) {
    try {
        const response = await fetch(`${API_BASE}/images/process-sample/${sampleName}`, {
            method: 'POST'
        });

        if (response.ok) {
            fetchAllData();
        } else {
            const err = await response.json();
            alert(`Error processing sample: ${err.detail}`);
        }
    } catch (e) {
        console.error("Error triggering sample analysis:", e);
    }
}

async function runFullTestSuite() {
    if (runAllSamplesBtn) {
        runAllSamplesBtn.disabled = true;
        runAllSamplesBtn.textContent = "Processing Field Dataset...";
    }
    await uploadSampleByName('user_sample_1.jpg');
    await uploadSampleByName('user_sample_2.jpg');
    await uploadSampleByName('user_sample_3.jpg');
    setTimeout(() => {
        fetchAllData();
        if (runAllSamplesBtn) {
            runAllSamplesBtn.disabled = false;
            runAllSamplesBtn.textContent = "Run Full Test Suite";
        }
    }, 1500);
}

async function clearAllQueueItems() {
    if (!confirm('Are you sure you want to clear all processing queue records?')) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/images/clear-all`, { method: 'DELETE' });
        if (res.ok) {
            fetchAllData();
        } else {
            alert('Failed to clear queue.');
        }
    } catch (e) {
        console.error("Failed to clear queue:", e);
    }
}

async function deleteSingleImage(event, imageId) {
    event.stopPropagation();
    if (!confirm('Delete this image record?')) {
        return;
    }
    try {
        const res = await fetch(`${API_BASE}/images/${imageId}`, { method: 'DELETE' });
        if (res.ok) {
            fetchAllData();
        } else {
            alert('Failed to delete image record.');
        }
    } catch (e) {
        console.error("Failed to delete image:", e);
    }
}

async function fetchAllData() {
    await Promise.all([fetchImageList(), fetchAnalyticsSummary()]);
}

async function fetchImageList() {
    const status = statusFilter.value;
    let url = `${API_BASE}/images?limit=50`;
    if (status) {
        url += `&status=${status}`;
    }

    try {
        const response = await fetch(url);
        const images = await response.json();
        renderImageList(images);
    } catch (err) {
        console.error('Failed to fetch image list:', err);
    }
}

async function fetchAnalyticsSummary() {
    try {
        const response = await fetch(`${API_BASE}/analytics/summary`);
        const summary = await response.json();

        statTotal.textContent = summary.total_images;
        statPass.textContent = summary.pass_count;
        statWarning.textContent = summary.warning_count;
        statReject.textContent = summary.reject_count;
    } catch (err) {
        console.error('Failed to fetch analytics:', err);
    }
}

function renderImageList(images) {
    if (!images || images.length === 0) {
        imageList.innerHTML = `<div class="empty-state"><p>No vehicle images found in processing queue.</p></div>`;
        return;
    }

    imageList.innerHTML = images.map(img => {
        const dateStr = new Date(img.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        
        let verdictBadge = '';
        let plateBadge = '';
        if (img.analysis) {
            const v = img.analysis.overall_verdict;
            const cls = v === 'PASS' ? 'badge-pass' : (v === 'WARNING' ? 'badge-warning' : 'badge-reject');
            verdictBadge = `<span class="badge ${cls}">${v}</span>`;
            if (img.analysis.detected_plate) {
                plateBadge = `<span class="badge badge-status" style="font-weight: 700; color: #4f46e5; border-color: rgba(79,70,229,0.3);">Plate: ${escapeHtml(img.analysis.detected_plate)}</span>`;
            }
        }

        const statusLabel = img.status === 'completed' ? 'Completed' : (img.status === 'processing' ? 'Processing' : img.status);
        const statusBadge = `<span class="badge badge-${img.status}">${statusLabel}</span>`;

        return `
            <div class="queue-item" onclick="openDetailModal('${img.id}')">
                <div class="item-left">
                    <img src="${API_BASE}/images/${img.id}/file" class="item-thumb" alt="Thumb" onerror="this.src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'44\' height=\'44\'><rect width=\'100%\' height=\'100%\' fill=\'%23e2e8f0\'/></svg>'">
                    <div class="item-info">
                        <span class="item-title">${escapeHtml(img.filename)}</span>
                        <span class="item-meta">ID: ${img.id.substring(0, 8)}... • ${dateStr} • ${(img.file_size / 1024).toFixed(1)} KB</span>
                    </div>
                </div>
                <div class="item-right" style="display: flex; gap: 8px; align-items: center;">
                    ${plateBadge}
                    ${verdictBadge}
                    ${statusBadge}
                    <button class="btn btn-icon btn-delete" onclick="deleteSingleImage(event, '${img.id}')" title="Delete image">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

async function openDetailModal(imageId) {
    modalBodyContent.innerHTML = `<p style="text-align:center; padding: 40px; color: var(--text-muted);">Loading inspection report...</p>`;
    detailModal.classList.remove('hidden');

    try {
        const response = await fetch(`${API_BASE}/images?limit=100`);
        const list = await response.json();
        const img = list.find(i => i.id === imageId);

        if (!img) {
            modalBodyContent.innerHTML = `<p>Image record not found.</p>`;
            return;
        }

        let resultHtml = '';
        if (img.analysis) {
            const a = img.analysis;
            const verdictCls = a.overall_verdict === 'PASS' ? 'badge-pass' : (a.overall_verdict === 'WARNING' ? 'badge-warning' : 'badge-reject');
            
            const flaggedList = a.flagged_issues.length > 0 
                ? a.flagged_issues.map(issue => `<li style="color: #dc2626; background: #fee2e2; padding: 8px 12px; border-radius: 6px; font-weight: 500;">- ${escapeHtml(issue)}</li>`).join('')
                : `<li style="color: #059669; background: #d1fae5; padding: 8px 12px; border-radius: 6px; font-weight: 500;">No quality anomalies detected. All thresholds satisfied.</li>`;

            resultHtml = `
                <div style="margin-top: 20px; border-top: 1px solid var(--border-color); padding-top: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                        <h3 style="font-size: 14px; font-weight: 600; color: var(--text-main);">Quality Analysis Results</h3>
                        <span class="badge ${verdictCls}" style="font-size: 12px; padding: 4px 10px;">VERDICT: ${a.overall_verdict}</span>
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 12px;">
                        <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
                            <span style="color: var(--text-muted); display: block; font-size: 11px; font-weight: 600;">LAPLACIAN BLUR VARIANCE</span>
                            <strong style="font-size: 15px; color: ${a.is_blurry ? '#dc2626' : '#059669'};">${a.blur_score}</strong>
                            <span style="font-size: 11px; display: block; margin-top: 2px; color: var(--text-sub);">${a.is_blurry ? 'Blurry (< 100.0)' : 'Sharp'}</span>
                        </div>
                        <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
                            <span style="color: var(--text-muted); display: block; font-size: 11px; font-weight: 600;">MEAN LUMINANCE (HSV)</span>
                            <strong style="font-size: 15px; color: ${a.is_low_light ? '#d97706' : '#059669'};">${a.brightness_score}</strong>
                            <span style="font-size: 11px; display: block; margin-top: 2px; color: var(--text-sub);">${a.is_low_light ? 'Low Light (< 45.0)' : 'Optimal Lighting'}</span>
                        </div>
                        <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
                            <span style="color: var(--text-muted); display: block; font-size: 11px; font-weight: 600;">DETECTED LICENSE PLATE</span>
                            <strong style="font-size: 15px; color: #4f46e5;">${a.detected_plate || 'None Detected'}</strong>
                            <span style="font-size: 11px; display: block; margin-top: 2px; color: var(--text-sub);">${a.is_valid_plate ? 'Valid Registration Format' : 'Non-Standard Format'}</span>
                        </div>
                        <div style="background: #f8fafc; padding: 12px; border-radius: 6px; border: 1px solid var(--border-color);">
                            <span style="color: var(--text-muted); display: block; font-size: 11px; font-weight: 600;">PERCEPTUAL HASH (dHash)</span>
                            <strong style="font-size: 13px; color: ${a.is_duplicate ? '#dc2626' : '#059669'};">${a.is_duplicate ? 'Duplicate Match' : 'Unique Image'}</strong>
                            <span style="font-size: 11px; display: block; margin-top: 2px; color: var(--text-sub);">${a.duplicate_of_id ? `Matches ID: ${a.duplicate_of_id.substring(0,8)}` : 'No Duplicates Found'}</span>
                        </div>
                    </div>

                    <h4 style="margin-top: 18px; margin-bottom: 10px; font-size: 13px; font-weight: 600; color: var(--text-main);">Flagged Pipeline Issues</h4>
                    <ul style="list-style: none; font-size: 12px; display: flex; flex-direction: column; gap: 6px;">
                        ${flaggedList}
                    </ul>
                </div>
            `;
        } else {
            resultHtml = `<p style="margin-top: 20px; color: var(--text-muted); text-align: center;">Processing in background queue...</p>`;
        }

        modalBodyContent.innerHTML = `
            <h2 style="font-size: 16px; margin-bottom: 4px; font-weight: 700; color: var(--text-main);">Inspection Record: ${escapeHtml(img.filename)}</h2>
            <p style="font-size: 11px; color: var(--text-muted); margin-bottom: 14px;">Image ID: ${img.id} • Status: <span class="badge badge-${img.status}">${img.status}</span></p>
            
            <div style="text-align: center; background: #f1f5f9; padding: 10px; border-radius: 8px; border: 1px solid var(--border-color);">
                <img src="${API_BASE}/images/${img.id}/file" style="max-width: 100%; max-height: 300px; border-radius: 6px; object-fit: contain;">
            </div>

            ${resultHtml}
        `;

    } catch (err) {
        modalBodyContent.innerHTML = `<p style="color: red;">Failed to load report details.</p>`;
    }
}

function closeModal() {
    detailModal.classList.add('hidden');
}

function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
