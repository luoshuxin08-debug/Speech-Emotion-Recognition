#!/usr/bin/env python3
"""
语音情感识别后端 API
Flask 应用
"""

import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

# 添加项目根目录到路径
import sys
sys.path.insert(0, os.path.dirname(__file__))

from model_wrapper import get_predictor


app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# 配置
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB 最大上传
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

# 允许的音频文件扩展名
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'flac', 'm4a', 'aac'}

# 确保上传文件夹存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 存储历史记录
history = []


def allowed_file(filename):
    """检查文件扩展名"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """主页"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/api/models', methods=['GET'])
def get_models():
    """获取可用模型列表"""
    predictor = get_predictor()
    models = predictor.get_available_models()
    return jsonify({
        'success': True,
        'models': models
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """预测音频情感"""
    # 检查请求中是否有文件
    if 'audio' not in request.files:
        return jsonify({
            'success': False,
            'error': '没有上传文件'
        }), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': '未选择文件'
        }), 400
    
    # 获取模型选择
    model_id = request.form.get('model', 'cnn1d_librosa')
    
    if file and allowed_file(file.filename):
        # 保存文件
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        try:
            # 预测
            predictor = get_predictor()
            result = predictor.predict(filepath, model_id)
            
            # 保存历史记录
            if result.get('success'):
                history_item = {
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.now().isoformat(),
                    'filename': filename,
                    'result': result
                }
                history.insert(0, history_item)
                # 只保留最近20条记录
                if len(history) > 20:
                    history.pop()
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'处理失败: {str(e)}'
            }), 500
        finally:
            # 清理临时文件
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except:
                pass
    
    return jsonify({
        'success': False,
        'error': '不支持的文件格式'
    }), 400


@app.route('/api/history', methods=['GET'])
def get_history():
    """获取历史记录"""
    return jsonify({
        'success': True,
        'history': history
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'success': True,
        'status': 'ok'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🎤 语音情感识别系统 - Web 应用")
    print("=" * 60)
    print("\n正在启动服务器...")
    print("请在浏览器中访问: http://localhost:5000")
    print("\n按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 预热加载模型
    print("\n正在预加载模型...")
    predictor = get_predictor()
    for model_id in ['cnn1d_librosa']:
        success, msg = predictor.load_model(model_id)
        print(f"  - {model_id}: {msg}")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
