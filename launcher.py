#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映素材库下载器 - UI风格选择器
=============================

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

让用户选择喜欢的界面风格
"""

import os
import sys
import subprocess


def show_ui_options():
    """显示UI选项"""
    print("剪映素材库下载器 Pro - UI风格选择")
    print("=" * 40)
    print()
    print("可用的界面风格:")
    print()
    print("1. 标准版 (推荐)")
    print("   - 使用 = 符号和emoji")
    print("   - 现代美观的界面")
    print("   - 彩色和图标丰富")
    print()
    print("2. 简洁版")
    print("   - 使用 - 符号")
    print("   - 简洁现代风格")
    print("   - 适中的装饰")
    print()
    print("3. 极简版")
    print("   - 纯文本界面")
    print("   - 最高兼容性")
    print("   - 适合老旧终端")
    print()
    print("0. 退出")
    print()


def main():
    """主函数"""
    # 清屏
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        show_ui_options()
        
        choice = input("请选择界面风格 (0-3): ").strip()
        
        if choice == "0":
            print("退出程序")
            break
        elif choice == "1":
            print("启动标准版界面...")
            subprocess.run([sys.executable, "main.py"])
            break
        elif choice == "2":
            print("启动简洁版界面...")
            subprocess.run([sys.executable, "main_simple.py"])
            break
        elif choice == "3":
            print("启动极简版界面...")
            subprocess.run([sys.executable, "main_minimal.py"])
            break
        else:
            print("无效选择，请输入 0-3")
            input("按回车继续...")
            os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    main()
