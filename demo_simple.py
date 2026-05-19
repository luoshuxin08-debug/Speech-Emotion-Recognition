#!/usr/bin/env python3
"""
简化版演示脚本 - 不依赖外部库
展示项目结构和内容
"""

import os

def print_separator(title=""):
    """打印分隔符"""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)

def print_system_info():
    """打印系统信息"""
    print_separator("语音情感识别系统 - 复现指南")
    print("""
    项目概述：
    - 基于深度学习的语音情感识别
    - 支持多种模型 (CNN1D, LSTM, SVM, MLP)
    - 支持多种特征提取方法 (Librosa, OpenSmile)
    - 识别准确率约 80%

    支持的情感类别：
    - angry (愤怒)
    - fear (恐惧)
    - happy (快乐)
    - neutral (中性)
    - sad (悲伤)
    - surprise (惊讶)

    文件说明：
    - train.py          - 训练模型
    - predict.py        - 预测脚本
    - preprocess.py     - 特征提取
    - demo.py           - 演示脚本
    - predict_enhanced.py - 增强版预测脚本
    - REPRODUCTION_GUIDE.md - 详细复现指南
    """)

def show_directory_tree(start_path, prefix=""):
    """展示目录树"""
    if not os.path.exists(start_path):
        return
    
    items = sorted(os.listdir(start_path))
    for i, item in enumerate(items):
        path = os.path.join(start_path, item)
        is_last = i == len(items) - 1
        
        current_prefix = prefix + ("└── " if is_last else "├── ")
        print(f"{current_prefix}{item}")
        
        if os.path.isdir(path) and not item.startswith('.'):
            extension = "    " if is_last else "│   "
            show_directory_tree(path, prefix + extension)

def show_project_structure():
    """展示项目结构"""
    print_separator("项目结构")
    show_directory_tree("/workspace")

def show_available_models():
    """展示可用的预训练模型"""
    print_separator("可用的预训练模型")
    
    checkpoint_dir = "/workspace/checkpoints"
    if not os.path.exists(checkpoint_dir):
        print("  checkpoints 目录不存在")
        return
    
    models = set()
    for f in os.listdir(checkpoint_dir):
        if f.endswith('.h5') or f.endswith('.json') or f.endswith('.m'):
            if not f.startswith('SCALER'):
                model_name = os.path.splitext(f)[0]
                models.add(model_name)
    
    if models:
        print("\n  预训练模型列表：")
        for i, model in enumerate(sorted(models), 1):
            print(f"    {i}. {model}")
        
        print("\n  模型说明：")
        print("    - CNN1D_LIBROSA_IS10:   使用 Librosa 特征的 1维CNN 模型")
        print("    - CNN1D_OPENSMILE_IS10: 使用 OpenSmile 特征的 1维CNN 模型")
        print("    - LSTM_LIBROSA_IS10:    使用 Librosa 特征的 LSTM 模型")
        print("    - LSTM_OPENSMILE_IS10:  使用 OpenSmile 特征的 LSTM 模型")
        print("    - SVM_LIBROSA_IS10:     使用 Librosa 特征的 SVM 模型")
        print("    - SVM_OPENSMILE_IS10:   使用 OpenSmile 特征的 SVM 模型")
        print("    - MLP_LIBROSA_IS10:     使用 Librosa 特征的 MLP 模型")
        print("    - MLP_OPENSMILE_IS10:   使用 OpenSmile 特征的 MLP 模型")
    else:
        print("  没有找到预训练模型")

def show_config_files():
    """展示配置文件"""
    print_separator("配置文件")
    
    config_dir = "/workspace/configs"
    if os.path.exists(config_dir):
        for f in sorted(os.listdir(config_dir)):
            if f.endswith('.yaml'):
                print(f"\n  {f}:")
                try:
                    with open(os.path.join(config_dir, f), 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        for line in lines[:15]:  # 只显示前15行
                            print(f"    {line.rstrip()}")
                        if len(lines) > 15:
                            print(f"    ... (更多内容省略)")
                except Exception as e:
                    print(f"    无法读取: {e}")

def show_quick_start():
    """显示快速开始指南"""
    print_separator("快速开始")
    print("""
    1. 环境准备 (推荐 Python 3.9 或 3.10)：
    
       python -m venv venv
       source venv/bin/activate  # Linux/macOS
       pip install -r requirements.txt
    
    2. 使用预训练模型预测：
    
       # 编辑 predict.py 中的音频路径
       python predict.py --config configs/cnn1d.yaml
    
       或使用增强版：
       python predict_enhanced.py --config configs/cnn1d.yaml --audio your_audio.wav
    
    3. 重新训练模型 (需要数据集)：
    
       python preprocess.py --config configs/cnn1d.yaml
       python train.py --config configs/cnn1d.yaml
    
    4. 配置说明：
    
       配置文件位于 configs/ 目录，关键参数：
       - model: 模型类型 (cnn1d/lstm/svm/mlp)
       - feature_method: 特征类型 (l=librosa, o=opensmile)
       - class_labels: 情感类别
       - checkpoint_name: 模型文件名
    
    详细说明请查看 REPRODUCTION_GUIDE.md
    """)

def main():
    """主函数"""
    print_system_info()
    show_project_structure()
    show_available_models()
    show_config_files()
    show_quick_start()
    
    print_separator()
    print("""
    完成！项目已准备就绪。
    
    下一步：
    1. 阅读 REPRODUCTION_GUIDE.md 了解详细信息
    2. 准备兼容的 Python 环境 (3.8-3.11)
    3. 安装依赖并开始使用！
    """)

if __name__ == "__main__":
    main()
