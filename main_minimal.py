#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映素材库下载器 - 启动脚本 (极简版UI)
===================================

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

最简洁的命令行界面，兼容所有终端
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
    """打印启动横幅 - 极简版"""
    # 清屏
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("剪映素材库下载器 Pro v2.0.0")
    print("JianYing Downloader Pro")
    print("")
    print("功能: 智能搜索 | 批量下载 | 多分辨率 | 断点续传")
    print("作者: Akikai | 更新: 2025年6月30日")
    print("")


def check_environment():
    """检查运行环境"""
    print("检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
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
        print(f"错误: 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("环境检查通过")
    return True


def setup_config():
    """设置配置"""
    config_manager = ConfigManager()
    
    # 检查是否已配置Cookie
    if not config_manager.is_cookies_configured():
        print("")
        print("警告: 未检测到Cookie配置")
        print("")
        print("请按照以下步骤配置Cookie:")
        print("1. 访问 https://www.jianying.com")
        print("2. 打开开发者工具 (F12)")
        print("3. 在Network标签中找到搜索请求")
        print("4. 复制Cookie信息到 config/settings.json")
        print("")
        
        example_config = {
            "cookies": {
                "sessionid": "your_session_id",
                "sid_tt": "your_sid_tt",
                "sid_guard": "your_sid_guard"
            }
        }
        print("配置示例:")
        print(json.dumps(example_config, indent=2, ensure_ascii=False))
        print("")
        
        # 询问是否继续
        choice = input("是否要继续？(y/N): ").strip().lower()
        if choice not in ['y', 'yes']:
            return None
    
    return config_manager


def interactive_download():
    """交互式下载 - 极简版"""
    print("")
    print("功能菜单")
    print("--------")
    print("1. 单个关键词下载")
    print("2. 批量关键词下载") 
    print("3. 自定义配置下载")
    print("4. 查看下载状态")
    print("0. 退出")
    print("")
    
    while True:
        choice = input("请选择 (0-4): ").strip()
        
        if choice == "0":
            print("感谢使用!")
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
            print("无效选择，请输入 0-4")


def single_keyword_download():
    """单个关键词下载 - 极简版"""
    print("")
    print("单个关键词下载")
    print("-------------")
    
    keyword = input("请输入关键词: ").strip()
    if not keyword:
        print("错误: 关键词不能为空")
        return True
    
    try:
        max_pages = int(input("最大页数 (默认5): ") or "5")
    except ValueError:
        max_pages = 5
    
    # 创建下载器
    config_manager = ConfigManager()
    config_manager.set(max_pages, "search", "max_pages")
    
    downloader = JianyingDownloader(config_manager)
    
    print(f"开始下载: {keyword}")
    try:
        stats = downloader.download_keyword_videos(keyword)
        print("")
        print("下载完成!")
        print(f"找到视频: {stats['total_found']}")
        print(f"成功下载: {stats['total_downloaded']}")
        print(f"下载失败: {stats['failed_downloads']}")
    except Exception as e:
        print(f"下载失败: {e}")
    
    return True


def batch_download():
    """批量下载 - 极简版"""
    print("")
    print("批量关键词下载")
    print("-------------")
    
    print("输入关键词 (每行一个，空行结束):")
    keywords = []
    while True:
        keyword = input(f"关键词 {len(keywords) + 1}: ").strip()
        if not keyword:
            break
        keywords.append(keyword)
    
    if not keywords:
        print("错误: 未输入任何关键词")
        return True
    
    # 创建下载器
    config_manager = ConfigManager()
    config_manager.set(keywords, "search", "keywords")
    
    downloader = JianyingDownloader(config_manager)
    
    print(f"开始批量下载 ({len(keywords)} 个关键词)")
    try:
        stats = downloader.batch_download()
        print("")
        print("批量下载完成!")
        print(f"处理关键词: {stats['completed_keywords']}/{stats['total_keywords']}")
        print(f"总计下载: {stats['total_downloaded']}/{stats['total_found']}")
    except Exception as e:
        print(f"下载失败: {e}")
    
    return True


def custom_download():
    """自定义配置下载 - 极简版"""
    print("")
    print("自定义配置下载")
    print("-------------")
    
    config_manager = ConfigManager()
    
    # 配置选项
    download_dir = input(f"下载目录 (当前: {config_manager.get('download', 'download_dir')}): ").strip()
    if download_dir:
        config_manager.set(download_dir, "download", "download_dir")
    
    resolution = input(f"分辨率 [1080p/720p/480p/360p] (当前: {config_manager.get('download', 'preferred_resolution')}): ").strip()
    if resolution:
        config_manager.set(resolution, "download", "preferred_resolution")
    
    try:
        max_workers = input(f"并发数 (当前: {config_manager.get('download', 'max_workers')}): ").strip()
        if max_workers:
            config_manager.set(int(max_workers), "download", "max_workers")
    except ValueError:
        pass
    
    # 输入关键词
    print("输入关键词:")
    keywords = []
    while True:
        keyword = input(f"关键词 {len(keywords) + 1}: ").strip()
        if not keyword:
            break
        keywords.append(keyword)
    
    if not keywords:
        print("错误: 未输入任何关键词")
        return True
    
    config_manager.set(keywords, "search", "keywords")
    
    # 开始下载
    downloader = JianyingDownloader(config_manager)
    
    print("开始自定义下载")
    try:
        stats = downloader.batch_download()
        print(f"下载完成: {stats['total_downloaded']}/{stats['total_found']}")
    except Exception as e:
        print(f"下载失败: {e}")
    
    return True


def show_download_status():
    """显示下载状态 - 极简版"""
    print("")
    print("下载状态")
    print("-------")
    
    config_manager = ConfigManager()
    downloader = JianyingDownloader(config_manager)
    
    try:
        status = downloader.get_download_status()
        
        if status["status"] == "未开始下载":
            print("还没有开始下载")
        else:
            print(f"下载目录: {status['download_dir']}")
            print(f"文件总数: {status['total_files']}")
            print(f"总大小: {status['total_size']}")
            print("")
            print("关键词统计:")
            for keyword, stats in status["keyword_stats"].items():
                print(f"  {keyword}: {stats['videos']} 视频, {stats['covers']} 封面")
    
    except Exception as e:
        print(f"获取状态失败: {e}")
    
    input("按回车继续...")
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
        print("")
        print("用户取消操作")
    except Exception as e:
        print(f"程序异常: {e}")
        logging.exception("程序异常")


if __name__ == "__main__":
    main()
