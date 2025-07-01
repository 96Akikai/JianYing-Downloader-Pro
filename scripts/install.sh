#!/bin/bash

echo "==============================================="
echo "   🎬 剪映素材库下载器 Pro - 一键安装脚本"
echo "==============================================="
echo

echo "🔍 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 未找到Python，请先安装Python 3.7或更高版本"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✅ Python环境检查通过"

echo
echo "📦 安装依赖包..."
if ! $PYTHON_CMD -m pip install -r requirements.txt; then
    echo "❌ 依赖安装失败，请检查网络连接"
    exit 1
fi

echo "✅ 依赖安装完成"

echo
echo "📁 创建必要目录..."
mkdir -p downloads
mkdir -p logs

echo "✅ 目录创建完成"

echo
echo "⚙️ 配置检查..."
if [ ! -f "config/settings.json" ]; then
    echo "⚠️  配置文件不存在，将使用默认配置"
    echo "🔧 请编辑 config/settings.json 文件来配置Cookie"
fi

echo
echo "==============================================="
echo "   ✅ 安装完成！"
echo "==============================================="
echo
echo "📝 下一步操作:"
echo "1. 编辑 config/settings.json 文件"
echo "2. 在其中配置您的Cookie信息"
echo "3. 运行: $PYTHON_CMD main.py"
echo
echo "📋 Cookie获取方法:"
echo "1. 访问 https://www.jianying.com"
echo "2. 按F12打开开发者工具"
echo "3. 在Network标签中找到搜索请求"
echo "4. 复制Cookie信息到配置文件中"
echo

read -p "按回车键退出..."
