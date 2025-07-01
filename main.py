#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映素材库下载器 - 启动脚本
=========================

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

提供简单易用的命令行界面
"""

import os
import sys
import json
import logging
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import JianyingDownloader, ConfigManager, setup_logging


def print_banner():
    """打印启动横幅"""
    # 清屏
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 方案1: 简洁现代风格
    banner = """
🎬 ================================= 🎬
    剪映素材库下载器 Pro v2.0.0
    JianYing Downloader Pro
🎬 ================================= 🎬

✨ 特性亮点:
   🔍 智能搜索     📥 批量下载
   🎭 多分辨率     🔄 断点续传
   ⚡ 并发下载     📊 统计报告

👨‍💻 作者: Akikai
📅 更新: 2025年6月30日
    """
    print(banner)


def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("❌ 需要Python 3.7或更高版本")
        return False
    
    # 检查必要的库
    required_packages = ['requests', 'tqdm']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 环境检查通过")
    return True


def setup_config():
    """设置配置"""
    config_manager = ConfigManager()
    
    # 检查是否已配置Cookie
    if not config_manager.is_cookies_configured():
        print("\n" + "🔧 " + "="*48 + " 🔧")
        print("              ⚠️  Cookie配置提醒")
        print("🔧 " + "="*48 + " 🔧")
        print("\n📋 请按照以下步骤配置Cookie:")
        print("   1️⃣  访问 https://www.jianying.com")
        print("   2️⃣  打开开发者工具 (按F12)")
        print("   3️⃣  在Network标签中找到搜索请求")
        print("   4️⃣  复制Cookie信息到 config/settings.json")
        print("\n💡 配置示例:")
        example_config = {
            "cookies": {
                "sessionid": "your_session_id",
                "sid_tt": "your_sid_tt",
                "sid_guard": "your_sid_guard"
            }
        }
        print("   " + json.dumps(example_config, indent=2, ensure_ascii=False).replace('\n', '\n   '))
        
        print("\n🔧 " + "="*48 + " 🔧")
        # 询问是否继续
        choice = input("\n❓ 是否要继续？(y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            return None
    
    return config_manager


def interactive_download():
    """交互式下载"""
    print("\n")
    print("🎯 " + "="*50 + " 🎯")
    print("              📋 功能选择菜单")
    print("🎯 " + "="*50 + " 🎯")
    print()
    print("   1️⃣  单个关键词下载    - 快速下载单个关键词")
    print("   2️⃣  批量关键词下载    - 下载多个关键词") 
    print("   3️⃣  自定义配置下载    - 临时修改配置")
    print("   4️⃣  查看下载状态      - 查看统计信息")
    print("   0️⃣  退出程序          - 安全退出")
    print()
    print("🎯 " + "="*50 + " 🎯")
    
    while True:
        choice = input("\n💡 请选择操作 (0-4): ").strip()
        
        if choice == "0":
            print("\n🎉 感谢使用剪映下载器 Pro！")
            print("👋 期待下次再见！")
            return False
        elif choice == "1":
            return single_keyword_download()
        elif choice == "2":
            return batch_download()
        elif choice == "3":
            return custom_download()
        elif choice == "4":
            return show_download_status()
        else:
            print("❌ 无效选择，请输入 0-4")


def single_keyword_download():
    """单个关键词下载"""
    print("\n📝 " + "="*40 + " 📝")
    print("           🎯 单个关键词下载")
    print("📝 " + "="*40 + " 📝")
    
    keyword = input("\n💭 请输入搜索关键词: ").strip()
    if not keyword:
        print("❌ 关键词不能为空")
        return True
    
    try:
        max_pages = int(input("📄 请输入最大页数 (默认5): ") or "5")
    except ValueError:
        max_pages = 5
    
    # 创建下载器
    config_manager = ConfigManager()
    config_manager.set(max_pages, "search", "max_pages")
    
    downloader = JianyingDownloader(config_manager)
    
    print(f"\n🚀 开始下载关键词: {keyword}")
    try:
        stats = downloader.download_keyword_videos(keyword)
        print(f"\n🎉 下载完成!")
        print(f"   📊 找到视频: {stats['total_found']}")
        print(f"   ✅ 成功下载: {stats['total_downloaded']}")
        print(f"   ❌ 下载失败: {stats['failed_downloads']}")
        print("\n📝 " + "="*40 + " 📝")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    
    return True


def batch_download():
    """批量下载"""
    print("\n📦 " + "="*40 + " 📦")
    print("           🎯 批量关键词下载")
    print("📦 " + "="*40 + " 📦")
    
    print("\n💭 请输入搜索关键词 (每行一个，输入空行结束):")
    keywords = []
    while True:
        keyword = input(f"   关键词 {len(keywords) + 1}: ").strip()
        if not keyword:
            break
        keywords.append(keyword)
    
    if not keywords:
        print("❌ 未输入任何关键词")
        return True
    
    # 创建下载器
    config_manager = ConfigManager()
    config_manager.set(keywords, "search", "keywords")
    
    downloader = JianyingDownloader(config_manager)
    
    print(f"\n🚀 开始批量下载 {len(keywords)} 个关键词")
    try:
        stats = downloader.batch_download()
        print(f"\n🎉 批量下载完成!")
        print(f"   📋 处理关键词: {stats['completed_keywords']}/{stats['total_keywords']}")
        print(f"   📊 找到视频: {stats['total_found']}")
        print(f"   ✅ 成功下载: {stats['total_downloaded']}")
        print(f"   ❌ 下载失败: {stats['total_failed']}")
        print("\n📦 " + "="*40 + " 📦")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    
    return True


def custom_download():
    """自定义配置下载"""
    print("\n⚙️  " + "="*40 + " ⚙️")
    print("           🎯 自定义配置下载")
    print("⚙️  " + "="*40 + " ⚙️")
    
    config_manager = ConfigManager()
    
    # 配置下载目录
    download_dir = input(f"\n📁 下载目录 (当前: {config_manager.get('download', 'download_dir')}): ").strip()
    if download_dir:
        config_manager.set(download_dir, "download", "download_dir")
    
    # 配置分辨率
    print("\n🎭 分辨率选项: 1080p, 720p, 480p, 360p, origin")
    resolution = input(f"   首选分辨率 (当前: {config_manager.get('download', 'preferred_resolution')}): ").strip()
    if resolution:
        config_manager.set(resolution, "download", "preferred_resolution")
    
    # 配置并发数
    try:
        max_workers = input(f"\n⚡ 并发下载数 (当前: {config_manager.get('download', 'max_workers')}): ").strip()
        if max_workers:
            config_manager.set(int(max_workers), "download", "max_workers")
    except ValueError:
        pass
    
    # 输入关键词
    print("\n💭 请输入搜索关键词:")
    keywords = []
    while True:
        keyword = input(f"   关键词 {len(keywords) + 1}: ").strip()
        if not keyword:
            break
        keywords.append(keyword)
    
    if not keywords:
        print("❌ 未输入任何关键词")
        return True
    
    config_manager.set(keywords, "search", "keywords")
    
    # 开始下载
    downloader = JianyingDownloader(config_manager)
    
    print(f"\n🚀 开始自定义下载")
    try:
        stats = downloader.batch_download()
        print(f"\n🎉 下载完成!")
        print(f"   ✅ 成功下载: {stats['total_downloaded']}/{stats['total_found']}")
        print("\n⚙️  " + "="*40 + " ⚙️")
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    
    return True


def show_download_status():
    """显示下载状态"""
    print("\n📊 " + "="*40 + " 📊")
    print("           🎯 下载状态统计")
    print("📊 " + "="*40 + " 📊")
    
    config_manager = ConfigManager()
    downloader = JianyingDownloader(config_manager)
    
    try:
        status = downloader.get_download_status()
        
        if status["status"] == "未开始下载":
            print("\n📝 还没有开始下载任何内容")
            print("💡 提示: 可以选择其他功能开始下载")
        else:
            print(f"\n📂 下载目录: {status['download_dir']}")
            print(f"📁 总文件数: {status['total_files']}")
            print(f"💾 总大小: {status['total_size']}")
            
            print(f"\n📋 各关键词详细统计:")
            for keyword, stats in status["keyword_stats"].items():
                print(f"   🎬 {keyword}: {stats['videos']} 视频, {stats['covers']} 封面")
        
        print("\n📊 " + "="*40 + " 📊")
    
    except Exception as e:
        print(f"❌ 获取状态失败: {e}")
    
    input("\n⏸️  按回车键继续...")
    return True


def main():
    """主函数"""
    print_banner()
    
    # 检查环境
    if not check_environment():
        return
    
    # 设置日志
    setup_logging(level="INFO", console_enabled=True, file_enabled=True)
    
    # 设置配置
    config_manager = setup_config()
    if not config_manager:
        return
    
    # 交互式下载
    try:
        while interactive_download():
            pass
    except KeyboardInterrupt:
        print("\n\n❌ 用户取消操作")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}")
        logging.exception("程序异常")


if __name__ == "__main__":
    main()
