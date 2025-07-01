@echo off
chcp 65001 >nul
title 剪映素材库下载器 Pro - 快速启动

echo.
echo 🎬 ================================= 🎬
echo     剪映素材库下载器 Pro v2.0.0
echo     JianYing Downloader Pro
echo 🎬 ================================= 🎬
echo.

echo 🔍 检查环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python或运行install.bat
    echo.
    pause
    exit /b 1
)

echo ✅ Python环境正常
echo.

echo 🎨 选择界面风格...
echo    1. 标准版 (推荐) - 现代美观界面
echo    2. 简洁版        - 简洁现代风格  
echo    3. 极简版        - 纯文本兼容性最好
echo    4. 自动选择      - 使用UI选择器
echo.

set /p ui_choice="请选择 (1-4, 默认1): "
if "%ui_choice%"=="" set ui_choice=1

if "%ui_choice%"=="1" (
    echo 🚀 启动标准版界面...
    python main.py
) else if "%ui_choice%"=="2" (
    echo 🚀 启动简洁版界面...
    python main_simple.py
) else if "%ui_choice%"=="3" (
    echo 🚀 启动极简版界面...
    python main_minimal.py
) else if "%ui_choice%"=="4" (
    echo 🚀 启动UI选择器...
    python launcher.py
) else (
    echo 🚀 启动默认界面...
    python main.py
)

echo.
echo 🎯 ================================= 🎯
echo         程序已退出，感谢使用！
echo 🎯 ================================= 🎯
pause >nul
