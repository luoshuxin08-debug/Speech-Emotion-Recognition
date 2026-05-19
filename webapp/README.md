# 语音情感识别系统 - Web应用

这是一个基于深度学习的语音情感识别Web应用，提供美观的用户界面和完整的分析功能。

## 功能特性

- 🎵 支持多种音频格式 (WAV, MP3, OGG, FLAC, M4A, AAC)
- 🤖 提供4种预训练模型 (CNN1D, LSTM, SVM, MLP)
- 📊 可视化分析结果 (柱状图、雷达图)
- 📜 历史记录功能
- 🎨 现代化响应式界面
- ⚡ 拖拽上传支持

## 系统要求

- Python 3.8 - 3.11 (推荐 3.9 或 3.10)
- 依赖包见根目录 `requirements.txt`
- 现代浏览器 (Chrome, Firefox, Safari, Edge)

## 快速开始

### 1. 安装依赖

首先在项目根目录安装项目依赖：

```bash
cd /path/to/project
pip install -r requirements.txt
```

然后安装Web应用额外依赖：

```bash
cd webapp
pip install -r requirements.txt
```

### 2. 启动应用

#### Linux/Mac:

```bash
cd webapp
./start.sh
```

或者直接运行：

```bash
cd webapp/backend
python app.py
```

#### Windows:

```cmd
cd webapp
start.bat
```

或者直接运行：

```cmd
cd webapp\backend
python app.py
```

### 3. 访问应用

打开浏览器，访问：`http://localhost:5000`

## 使用说明

### 1. 上传音频

- 点击上传区域或拖拽音频文件到上传框
- 支持的格式：WAV, MP3, OGG, FLAC, M4A, AAC

### 2. 选择模型

- CNN1D (推荐) - 一维卷积神经网络
- LSTM - 长短期记忆网络
- SVM - 支持向量机
- MLP - 多层感知机

### 3. 分析

点击"开始分析"按钮，等待处理完成。

### 4. 查看结果

- 主要识别结果和置信度
- 各类别概率分布柱状图
- 情感雷达图
- 详细信息和历史记录

## 项目结构

```
webapp/
├── backend/              # 后端代码
│   ├── app.py           # Flask应用主文件
│   ├── model_wrapper.py # 模型封装
│   ├── requirements.txt # Web后端依赖
│   └── uploads/         # 上传目录 (自动创建)
├── frontend/            # 前端代码
│   ├── index.html       # 主页面
│   ├── css/
│   │   └── style.css    # 样式文件
│   └── js/
│       └── app.js       # 前端逻辑
├── start.sh             # Linux/Mac启动脚本
├── start.bat            # Windows启动脚本
└── README.md            # 本文件
```

## API接口

### 获取可用模型

```
GET /api/models
```

响应:
```json
{
  "success": true,
  "models": [
    {
      "id": "cnn1d_librosa",
      "name": "1D CNN (Librosa特征)"
    }
  ]
}
```

### 预测情感

```
POST /api/predict
Content-Type: multipart/form-data

参数:
- audio: 音频文件
- model: 模型ID (可选，默认 cnn1d_librosa)
```

响应:
```json
{
  "success": true,
  "prediction": "happy",
  "prediction_cn": "快乐",
  "confidence": 0.85,
  "probabilities": {
    "angry": 0.05,
    "fear": 0.02,
    "happy": 0.85,
    "neutral": 0.03,
    "sad": 0.03,
    "surprise": 0.02
  },
  "class_labels": [...],
  "class_labels_cn": [...],
  "colors": [...],
  "model_used": "cnn1d_librosa",
  "model_name": "1D CNN (Librosa特征)"
}
```

### 获取历史记录

```
GET /api/history
```

### 健康检查

```
GET /api/health
```

## 支持的情感类别

- 😠 Angry (愤怒)
- 😨 Fear (恐惧)
- 😄 Happy (快乐)
- 😐 Neutral (中性)
- 😢 Sad (悲伤)
- 😲 Surprise (惊讶)

## 技术栈

### 后端
- Flask - Web框架
- TensorFlow/Keras - 深度学习框架
- Librosa - 音频特征提取

### 前端
- 原生 HTML5/CSS3/JavaScript
- Chart.js - 图表可视化

## 常见问题

### 1. TensorFlow/Python版本问题

确保使用 Python 3.8 - 3.11，TensorFlow 2.x。

### 2. 端口被占用

修改 `backend/app.py` 中的端口号，默认是 5000。

### 3. 模型加载失败

确保 `checkpoints/` 目录在项目根目录下，包含所有模型文件。

## 开发说明

### 本地开发

```bash
# 后端运行在 http://localhost:5000
cd webapp/backend
python app.py
```

### 调试模式

应用默认在 debug 模式运行，修改代码后自动重载。

## 许可证

与项目主体保持一致。
