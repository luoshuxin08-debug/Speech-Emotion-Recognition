@echo off
REM 启动语音情感识别Web应用 (Windows版本)

echo ============================================
echo 语音情感识别系统 - Web应用
echo ============================================
echo.

REM 检查Python版本
echo 检查Python版本...
python --version

REM 切换到项目根目录
cd /d "%~dp0.."

REM 创建上传目录
if not exist "webapp\backend\uploads" mkdir webapp\backend\uploads

echo.
echo 正在启动应用...
echo 请在浏览器中访问: http://localhost:5000
echo.
echo 按 Ctrl+C 停止服务器
echo ============================================
echo.

cd webapp\backend
python app.py

pause
