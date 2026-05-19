#!/usr/bin/env python3
"""
语音情感识别系统演示脚本
展示如何使用预训练模型进行预测
"""

import os
import sys
import numpy as np

def print_separator(title=""):
    """打印分隔符"""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)

def print_system_info():
    """打印系统信息"""
    print_separator("语音情感识别系统")
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
    """)

def show_available_models():
    """展示可用的预训练模型"""
    print_separator("可用的预训练模型")
    
    checkpoint_dir = "checkpoints"
    if not os.path.exists(checkpoint_dir):
        print("  checkpoints 目录不存在")
        return
    
    models = []
    for f in os.listdir(checkpoint_dir):
        if f.endswith('.h5') or f.endswith('.json') or f.endswith('.m'):
            if not f.startswith('SCALER'):
                model_name = os.path.splitext(f)[0]
                if model_name not in models:
                    models.append(model_name)
    
    if models:
        print("\n  预训练模型列表：")
        for i, model in enumerate(sorted(models), 1):
            print(f"    {i}. {model}")
    else:
        print("  没有找到预训练模型")

def show_feature_data():
    """展示已提取的特征数据"""
    print_separator("已提取的特征数据")
    
    feature_dir = "features"
    if not os.path.exists(feature_dir):
        print("  features 目录不存在")
        return
    
    print("\n  特征数据集：")
    for root, dirs, files in os.walk(feature_dir):
        level = root.replace(feature_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"  {indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for f in files:
            print(f"  {subindent}{f}")

def show_usage_example():
    """显示使用示例"""
    print_separator("使用示例")
    
    print("""
    1. 使用预训练模型预测：
    
       修改 predict.py 中的音频路径，然后运行：
         python predict.py --config configs/cnn1d.yaml
    
    2. 训练新模型：
    
       # 步骤1：准备数据集（按情感分类放置）
       # 步骤2：提取特征
         python preprocess.py --config configs/cnn1d.yaml
       # 步骤3：训练模型
         python train.py --config configs/cnn1d.yaml
    
    3. 配置文件说明：
    
       - configs/cnn1d.yaml    - 一维CNN模型配置
       - configs/lstm.yaml     - LSTM模型配置
       - configs/svm.yaml      - SVM模型配置
       - configs/mlp.yaml      - MLP模型配置
    
    4. 环境要求：
    
       - Python 3.8 - 3.11
       - TensorFlow 2.x
       - 详见 requirements.txt
    """)

def main():
    """主函数"""
    print_system_info()
    show_available_models()
    show_feature_data()
    show_usage_example()
    
    print_separator()
    print("""
    详细说明请查看：
    - REPRODUCTION_GUIDE.md (复现指南)
    - README.md (项目说明)
    """)

if __name__ == "__main__":
    main()
