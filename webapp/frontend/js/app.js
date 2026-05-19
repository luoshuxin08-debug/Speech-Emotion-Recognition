// 语音情感识别系统 - 前端逻辑
const API_BASE = '';

// 情感对应的 emoji
const EMOTION_EMOJI = {
    'angry': '😠',
    'fear': '😨',
    'happy': '😄',
    'neutral': '😐',
    'sad': '😢',
    'surprise': '😲'
};

// 情感对应的颜色
const EMOTION_COLORS = {
    'angry': '#ef4444',
    'fear': '#8b5cf6',
    'happy': '#f59e0b',
    'neutral': '#64748b',
    'sad': '#3b82f6',
    'surprise': '#10b981'
};

// 全局状态
let selectedFile = null;
let selectedModel = 'cnn1d_librosa';
let probabilityChart = null;
let radarChart = null;
let history = [];

// DOM 元素
const elements = {
    uploadArea: document.getElementById('uploadArea'),
    fileInput: document.getElementById('fileInput'),
    uploadBtn: document.getElementById('uploadBtn'),
    fileInfo: document.getElementById('fileInfo'),
    fileName: document.getElementById('fileName'),
    fileSize: document.getElementById('fileSize'),
    removeBtn: document.getElementById('removeBtn'),
    modelList: document.getElementById('modelList'),
    analyzeBtn: document.getElementById('analyzeBtn'),
    resultsSection: document.getElementById('resultsSection'),
    emotionIcon: document.getElementById('emotionIcon'),
    emotionName: document.getElementById('emotionName'),
    emotionConfidence: document.getElementById('emotionConfidence'),
    infoList: document.getElementById('infoList'),
    historyList: document.getElementById('historyList'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    toast: document.getElementById('toast')
};

// 工具函数
function showToast(message, type = 'success') {
    elements.toast.textContent = message;
    elements.toast.className = `toast ${type} show`;
    setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 3000);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// 初始化
async function init() {
    await loadModels();
    setupEventListeners();
}

// 加载模型列表
async function loadModels() {
    try {
        const response = await fetch(`${API_BASE}/api/models`);
        const data = await response.json();
        
        if (data.success) {
            renderModels(data.models);
        }
    } catch (error) {
        console.error('加载模型失败:', error);
    }
}

// 渲染模型列表
function renderModels(models) {
    elements.modelList.innerHTML = models.map((model, index) => `
        <div class="model-option ${index === 0 ? 'selected' : ''}" data-model="${model.id}">
            <input type="radio" name="model" value="${model.id}" id="model-${model.id}" ${index === 0 ? 'checked' : ''}>
            <label for="model-${model.id}">${model.name}</label>
        </div>
    `).join('');

    // 添加点击事件
    document.querySelectorAll('.model-option').forEach(option => {
        option.addEventListener('click', () => {
            document.querySelectorAll('.model-option').forEach(o => o.classList.remove('selected'));
            option.classList.add('selected');
            option.querySelector('input').checked = true;
            selectedModel = option.dataset.model;
        });
    });
}

// 设置事件监听
function setupEventListeners() {
    // 上传区域点击
    elements.uploadArea.addEventListener('click', () => {
        elements.fileInput.click();
    });

    // 按钮点击
    elements.uploadBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        elements.fileInput.click();
    });

    // 文件选择
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // 拖拽上传
    elements.uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.add('dragover');
    });

    elements.uploadArea.addEventListener('dragleave', () => {
        elements.uploadArea.classList.remove('dragover');
    });

    elements.uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    // 移除文件
    elements.removeBtn.addEventListener('click', () => {
        clearFile();
    });

    // 分析按钮
    elements.analyzeBtn.addEventListener('click', analyzeAudio);
}

// 处理文件选择
function handleFileSelect(file) {
    // 检查文件类型
    const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg', 'audio/ogg', 'audio/flac', 'audio/mp4', 'audio/x-m4a', 'audio/aac'];
    const allowedExtensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a', '.aac'];
    
    const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
        showToast('不支持的文件格式，请上传音频文件', 'error');
        return;
    }

    selectedFile = file;
    elements.fileName.textContent = file.name;
    elements.fileSize.textContent = formatFileSize(file.size);
    elements.fileInfo.style.display = 'block';
    elements.uploadArea.style.display = 'none';
    elements.analyzeBtn.disabled = false;

    showToast('文件已选择，点击开始分析');
}

// 清除文件
function clearFile() {
    selectedFile = null;
    elements.fileInput.value = '';
    elements.fileInfo.style.display = 'none';
    elements.uploadArea.style.display = 'block';
    elements.analyzeBtn.disabled = true;
    elements.resultsSection.style.display = 'none';
}

// 分析音频
async function analyzeAudio() {
    if (!selectedFile) return;

    // 显示加载状态
    elements.loadingOverlay.style.display = 'flex';
    elements.analyzeBtn.classList.add('loading');
    elements.analyzeBtn.disabled = true;

    try {
        const formData = new FormData();
        formData.append('audio', selectedFile);
        formData.append('model', selectedModel);

        const response = await fetch(`${API_BASE}/api/predict`, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            displayResults(result);
            addToHistory(selectedFile.name, result);
            showToast('分析完成！');
        } else {
            showToast(result.error || '分析失败', 'error');
        }
    } catch (error) {
        console.error('分析失败:', error);
        showToast('网络错误，请稍后重试', 'error');
    } finally {
        elements.loadingOverlay.style.display = 'none';
        elements.analyzeBtn.classList.remove('loading');
        elements.analyzeBtn.disabled = false;
    }
}

// 显示结果
function displayResults(result) {
    elements.resultsSection.style.display = 'flex';
    
    // 主结果
    const emotion = result.prediction;
    const emotionCn = result.prediction_cn;
    const confidence = result.confidence;

    elements.emotionIcon.textContent = EMOTION_EMOJI[emotion] || '🎵';
    elements.emotionName.textContent = emotionCn;
    elements.emotionName.style.color = EMOTION_COLORS[emotion];
    elements.emotionConfidence.textContent = `置信度: ${(confidence * 100).toFixed(1)}%`;

    // 详细信息
    renderInfoList(result);

    // 图表
    renderProbabilityChart(result);
    renderRadarChart(result);

    // 滚动到结果区域
    elements.resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// 渲染详细信息
function renderInfoList(result) {
    const items = [
        { label: '使用模型', value: result.model_name },
        { label: '识别结果', value: result.prediction_cn },
        { label: '置信度', value: `${(result.confidence * 100).toFixed(1)}%` }
    ];

    elements.infoList.innerHTML = items.map(item => `
        <div class="info-item">
            <span class="info-label">${item.label}</span>
            <span class="info-value">${item.value}</span>
        </div>
    `).join('');
}

// 渲染概率柱状图
function renderProbabilityChart(result) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');
    
    // 销毁之前的图表
    if (probabilityChart) {
        probabilityChart.destroy();
    }

    const labels = result.class_labels_cn;
    const data = Object.values(result.probabilities);
    const colors = result.colors;

    probabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '概率',
                data: data.map(d => d * 100),
                backgroundColor: colors,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `概率: ${context.parsed.y.toFixed(1)}%`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// 渲染雷达图
function renderRadarChart(result) {
    const ctx = document.getElementById('radarChart').getContext('2d');
    
    if (radarChart) {
        radarChart.destroy();
    }

    const labels = result.class_labels_cn;
    const data = Object.values(result.probabilities);
    const colors = result.colors;

    radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: '情感概率',
                data: data,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: colors,
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 1,
                    ticks: {
                        stepSize: 0.2,
                        callback: function(value) {
                            return (value * 100).toFixed(0) + '%';
                        }
                    }
                }
            }
        }
    });
}

// 添加到历史记录
function addToHistory(filename, result) {
    const item = {
        id: Date.now(),
        filename: filename,
        emotion: result.prediction,
        emotionCn: result.prediction_cn,
        confidence: result.confidence,
        timestamp: new Date().toLocaleString()
    };

    history.unshift(item);
    
    // 只保留最近 10 条
    if (history.length > 10) {
        history.pop();
    }

    renderHistory();
}

// 渲染历史记录
function renderHistory() {
    if (history.length === 0) {
        elements.historyList.innerHTML = '<p class="empty-history">暂无历史记录</p>';
        return;
    }

    elements.historyList.innerHTML = history.map(item => `
        <div class="history-item">
            <span class="history-emoji">${EMOTION_EMOJI[item.emotion]}</span>
            <div class="history-info">
                <div class="history-filename">${item.filename}</div>
                <div class="history-meta">
                    ${item.emotionCn} · ${(item.confidence * 100).toFixed(1)}% · ${item.timestamp}
                </div>
            </div>
        </div>
    `).join('');
}

// 启动应用
document.addEventListener('DOMContentLoaded', init);
