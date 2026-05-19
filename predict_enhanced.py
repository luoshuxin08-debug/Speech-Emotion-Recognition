#!/usr/bin/env python3
"""
增强版预测脚本
支持命令行参数指定音频文件路径
"""

import os
import argparse
import numpy as np
import extract_feats.opensmile as of
import extract_feats.librosa as lf
import models
import utils

def predict_single_audio(config, audio_path: str, model):
    """
    预测单个音频的情感
    
    Args:
        config: 配置项
        audio_path (str): 要预测的音频路径
        model: 加载的模型
    """
    print(f"\n正在分析音频: {audio_path}")
    
    if not os.path.exists(audio_path):
        print(f"错误: 音频文件不存在: {audio_path}")
        return
    
    if config.feature_method == 'o':
        # 使用 Opensmile 特征
        of.get_data(config, audio_path, train=False)
        test_feature = of.load_feature(config, train=False)
    elif config.feature_method == 'l':
        # 使用 Librosa 特征
        test_feature = lf.get_data(config, audio_path, train=False)
    
    # 预测
    result = model.predict(test_feature)
    result_prob = model.predict_proba(test_feature)
    
    # 显示结果
    emotion = config.class_labels[int(result)]
    
    print(f"\n{'='*60}")
    print(f"识别结果: {emotion.upper()}")
    print(f"{'='*60}")
    print("\n各类别概率:")
    for label, prob in zip(config.class_labels, result_prob):
        print(f"  {label:10s}: {prob:.4f} ({prob*100:.1f}%)")
    
    # 绘制雷达图
    try:
        utils.radar(result_prob, config.class_labels)
    except Exception as e:
        print(f"\n注意: 无法绘制雷达图: {e}")
        print("提示: 如果在无头环境中运行，可视化会被跳过")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='语音情感识别预测')
    parser.add_argument('--config', type=str, default='configs/cnn1d.yaml',
                        help='配置文件路径 (默认: configs/cnn1d.yaml)')
    parser.add_argument('--audio', type=str, required=True,
                        help='要预测的音频文件路径')
    
    args = parser.parse_args()
    
    # 加载配置
    config = utils.parse_opt()
    # 由于 parse_opt 使用 argparse，我们手动设置配置文件路径
    # 这里简化处理，直接使用 yaml 加载
    
    # 加载模型
    print(f"正在加载模型...")
    model = models.load(config)
    print(f"模型加载成功: {config.checkpoint_name}")
    
    # 预测
    predict_single_audio(config, args.audio, model)

if __name__ == '__main__':
    main()
