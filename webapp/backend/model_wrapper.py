#!/usr/bin/env python3
"""
模型封装模块
简化与现有模型的交互
"""

import os
import sys
import yaml
import numpy as np
from typing import Dict, List, Tuple

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import models
import extract_feats.librosa as librosa_feat


class SimpleConfig:
    """简化的配置类"""
    def __init__(self, config_dict: dict):
        for k, v in config_dict.items():
            if isinstance(v, dict):
                self.__dict__[k] = SimpleConfig(v)
            else:
                self.__dict__[k] = v


class EmotionPredictor:
    """情感预测器封装"""
    
    # 可用的模型配置
    AVAILABLE_MODELS = {
        'cnn1d_librosa': {
            'model': 'cnn1d',
            'checkpoint_name': 'CNN1D_LIBROSA_IS10',
            'feature_method': 'l',
            'feature_folder': 'features/6-category/librosa_casia/',
            'class_labels': ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
            'description': '1D CNN (Librosa特征)'
        },
        'lstm_librosa': {
            'model': 'lstm',
            'checkpoint_name': 'LSTM_LIBROSA_IS10',
            'feature_method': 'l',
            'feature_folder': 'features/6-category/librosa_casia/',
            'class_labels': ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
            'description': 'LSTM (Librosa特征)'
        },
        'svm_librosa': {
            'model': 'svm',
            'checkpoint_name': 'SVM_LIBROSA_IS10',
            'feature_method': 'l',
            'feature_folder': 'features/6-category/librosa_casia/',
            'class_labels': ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
            'description': 'SVM (Librosa特征)'
        },
        'mlp_librosa': {
            'model': 'mlp',
            'checkpoint_name': 'MLP_LIBROSA_IS10',
            'feature_method': 'l',
            'feature_folder': 'features/6-category/librosa_casia/',
            'class_labels': ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise'],
            'description': 'MLP (Librosa特征)'
        }
    }
    
    # 情感标签的中文翻译
    EMOTION_TRANSLATION = {
        'angry': '愤怒',
        'fear': '恐惧',
        'happy': '快乐',
        'neutral': '中性',
        'sad': '悲伤',
        'surprise': '惊讶'
    }
    
    # 情感标签对应的颜色
    EMOTION_COLORS = {
        'angry': '#ef4444',
        'fear': '#8b5cf6',
        'happy': '#f59e0b',
        'neutral': '#6b7280',
        'sad': '#3b82f6',
        'surprise': '#10b981'
    }
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.loaded_models = set()
    
    def get_available_models(self) -> List[Dict]:
        """获取可用模型列表"""
        result = []
        for key, config in self.AVAILABLE_MODELS.items():
            result.append({
                'id': key,
                'name': config['description'],
                'class_labels': config['class_labels']
            })
        return result
    
    def load_model(self, model_id: str) -> Tuple[bool, str]:
        """加载指定模型"""
        if model_id not in self.AVAILABLE_MODELS:
            return False, f"未知模型: {model_id}"
        
        if model_id in self.loaded_models:
            return True, "模型已加载"
        
        try:
            config_dict = self.AVAILABLE_MODELS[model_id].copy()
            config_dict['checkpoint_path'] = os.path.join(
                os.path.dirname(__file__), 
                '../../checkpoints'
            )
            config = SimpleConfig(config_dict)
            
            # 加载模型
            model = models.load(config)
            self.models[model_id] = (model, config)
            self.loaded_models.add(model_id)
            
            return True, "模型加载成功"
            
        except Exception as e:
            return False, f"模型加载失败: {str(e)}"
    
    def predict(self, audio_path: str, model_id: str = 'cnn1d_librosa') -> Dict:
        """预测音频情感"""
        # 确保模型已加载
        if model_id not in self.loaded_models:
            success, msg = self.load_model(model_id)
            if not success:
                return {'error': msg}
        
        model, config = self.models[model_id]
        
        try:
            # 提取特征
            feature_method = config.feature_method
            
            if feature_method == 'l':
                # 使用 Librosa 提取特征
                temp_config = SimpleConfig({
                    'feature_folder': config.feature_folder,
                    'checkpoint_path': config.checkpoint_path
                })
                
                # 提取特征
                librosa_feat.get_data(temp_config, audio_path, train=False)
                features = librosa_feat.load_feature(temp_config, train=False)
            else:
                return {'error': 'OpenSmile 特征提取暂不支持'}
            
            # 预测
            result_idx = model.predict(features)
            probabilities = model.predict_proba(features)
            
            # 确保 probabilities 是1D数组
            if hasattr(probabilities, 'shape') and len(probabilities.shape) > 1:
                probabilities = probabilities[0]
            
            # 构建结果
            emotion_idx = int(result_idx) if isinstance(result_idx, np.ndarray) else int(result_idx)
            emotion_label = config.class_labels[emotion_idx]
            
            # 构建概率字典
            prob_dict = {}
            for i, label in enumerate(config.class_labels):
                prob_dict[label] = float(probabilities[i])
            
            return {
                'success': True,
                'prediction': emotion_label,
                'prediction_cn': self.EMOTION_TRANSLATION.get(emotion_label, emotion_label),
                'confidence': float(probabilities[emotion_idx]),
                'probabilities': prob_dict,
                'class_labels': config.class_labels,
                'class_labels_cn': [self.EMOTION_TRANSLATION.get(l, l) for l in config.class_labels],
                'colors': [self.EMOTION_COLORS.get(l, '#6b7280') for l in config.class_labels],
                'model_used': model_id,
                'model_name': self.AVAILABLE_MODELS[model_id]['description']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'预测失败: {str(e)}'
            }


# 单例
_predictor = None

def get_predictor() -> EmotionPredictor:
    """获取预测器单例"""
    global _predictor
    if _predictor is None:
        _predictor = EmotionPredictor()
    return _predictor
