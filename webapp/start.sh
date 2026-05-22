#!/bin/bash
# 启动语音情感识别Web应用

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "============================================"
echo "语音情感识别系统 - Web应用"
echo "============================================"
echo ""

# 检查Python版本
echo "检查Python版本..."
python3 --version

# 确保在项目根目录 (webapp的上一级)
cd ..

# 创建上传目录
mkdir -p webapp/backend/uploads

# 启动应用
echo ""
echo "正在启动应用..."
echo "请在浏览器中访问: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "============================================"
echo ""

cd webapp/backend
python3 app.py
