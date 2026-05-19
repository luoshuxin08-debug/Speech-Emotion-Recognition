# 语音情感识别系统复现指南

## 项目概述

这是一个基于深度学习的语音情感识别系统，使用 Keras/TensorFlow 实现。支持多种模型和特征提取方法，准确率达 80% 左右。

## 环境要求

- **Python 版本**: 3.8 - 3.11 (推荐 3.9 或 3.10)
- **操作系统**: Linux / macOS / Windows

## 快速开始

### 1. 安装依赖

```bash
# 推荐使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 准备数据集（可选）

项目已包含预训练模型和提取好的特征，你可以直接使用。如需自己训练：

支持的数据集：
- RAVDESS (英文, 8种情绪)
- SAVEE (英文, 7种情绪)
- EMO-DB (德语, 7种情绪)
- CASIA (中文, 6种情绪)

数据集结构要求：
```
datasets/
└── CASIA/
    ├── angry/
    │   ├── audio1.wav
    │   └── audio2.wav
    ├── happy/
    ├── sad/
    ├── neutral/
    ├── fear/
    └── surprise/
```

### 3. 配置参数

在 `configs/` 目录下选择或修改配置文件：

- `cnn1d.yaml` - 一维CNN配置
- `lstm.yaml` - LSTM配置
- `svm.yaml` - SVM配置
- `mlp.yaml` - MLP配置

关键配置项：
```yaml
model: cnn1d  # 模型类型
class_labels: ["angry", "fear", "happy", "neutral", "sad", "surprise"]
feature_method: l  # l=librosa, o=opensmile
checkpoint_name: CNN1D_LIBROSA_IS10  # 模型文件名
```

### 4. 使用预训练模型预测

项目 `checkpoints/` 目录已包含预训练模型：

```bash
# 修改 predict.py 中的音频路径
python predict.py --config configs/cnn1d.yaml
```

### 5. 重新训练（可选）

```bash
# 1. 提取特征
python preprocess.py --config configs/cnn1d.yaml

# 2. 训练模型
python train.py --config configs/cnn1d.yaml
```

## 项目结构

```
Speech-Emotion-Recognition/
├── checkpoints/        # 预训练模型
├── configs/           # 配置文件
├── extract_feats/     # 特征提取
│   ├── librosa.py     # Librosa特征
│   └── opensmile.py   # OpenSmile特征
├── features/          # 提取的特征数据
├── models/            # 模型实现
│   ├── base.py        # 基类
│   ├── ml.py          # 机器学习模型
│   └── dnn/           # 深度学习模型
├── utils/             # 工具函数
├── train.py           # 训练脚本
├── predict.py         # 预测脚本
└── preprocess.py      # 预处理脚本
```

## 模型与特征组合

| 模型 | 特征 | 配置文件 | 模型文件 |
|------|------|----------|----------|
| CNN1D | Librosa | cnn1d.yaml (feature_method: l) | CNN1D_LIBROSA_IS10 |
| CNN1D | OpenSmile | cnn1d.yaml (feature_method: o) | CNN1D_OPENSMILE_IS10 |
| LSTM | Librosa | lstm.yaml (feature_method: l) | LSTM_LIBROSA_IS10 |
| LSTM | OpenSmile | lstm.yaml (feature_method: o) | LSTM_OPENSMILE_IS10 |
| SVM | Librosa | svm.yaml (feature_method: l) | SVM_LIBROSA_IS10 |
| SVM | OpenSmile | svm.yaml (feature_method: o) | SVM_OPENSMILE_IS10 |
| MLP | Librosa | mlp.yaml (feature_method: l) | MLP_LIBROSA_IS10 |
| MLP | OpenSmile | mlp.yaml (feature_method: o) | MLP_OPENSMILE_IS10 |

## 特征说明

### Librosa 特征
- 音高 (Pitch)
- 频谱质心
- MFCC (50维)
- 色谱图
- 梅尔频谱
- 频谱对比度
- 过零率
- 能量特征

### OpenSmile 特征集
- IS09_emotion (384维)
- IS10_paraling (1582维) - 默认
- IS11_speaker_state (4368维)
- IS12_speaker_trait (6125维)
- IS13_ComParE (6373维)
- ComParE_2016 (6373维)

## 常见问题

### Python 版本兼容性
当前项目使用较老的 TensorFlow 2.8，建议使用 Python 3.8-3.10。

### OpenSmile 安装
使用 OpenSmile 特征需要安装：
```bash
# 下载并编译 OpenSmile
# https://github.com/naxingyu/opensmile
```

### 内存不足
如果训练时内存不足，减小 batch_size。

## 工具函数

```python
import utils

# 绘制雷达图
utils.radar(probabilities, labels)

# 绘制波形图
utils.waveform(audio_path)

# 绘制频谱图
utils.spectrogram(audio_path)

# 播放音频
utils.play_audio(audio_path)
```

## 许可证

见 LICENSE 文件
