"""
剪映素材库下载器 - 生产版本
==========================

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

一个功能完整的剪映素材库下载工具，支持：
- 关键词搜索和批量下载
- 多分辨率选择
- 并发下载和断点续传
- 完整的日志记录和错误处理
- 灵活的配置管理

版本: 2.0.0
许可: MIT License
"""

__version__ = "2.0.0"
__author__ = "Akikai"
__license__ = "MIT"

from .downloader import JianyingDownloader
from .config_manager import ConfigManager
from .utils import setup_logging

__all__ = ["JianyingDownloader", "ConfigManager", "setup_logging"]
