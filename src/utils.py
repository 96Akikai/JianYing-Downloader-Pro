#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
============

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

提供日志设置、文件处理、网络请求等通用工具函数
"""

import os
import re
import time
import logging
import hashlib
import urllib3
from typing import Optional, Tuple, Dict, Any
from pathlib import Path
from datetime import datetime


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_enabled: bool = True,
    file_enabled: bool = True,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    设置日志记录
    
    Args:
        level: 日志级别
        log_file: 日志文件路径
        console_enabled: 是否启用控制台输出
        file_enabled: 是否启用文件输出
        format_string: 自定义格式字符串
    
    Returns:
        配置好的logger对象
    """
    # 禁用urllib3的警告
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    # 创建logger
    logger = logging.getLogger("jianying_downloader")
    logger.setLevel(getattr(logging, level.upper()))
    
    # 清除已有的处理器
    logger.handlers.clear()
    
    # 设置格式
    if not format_string:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(format_string)
    
    # 控制台处理器
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件处理器
    if file_enabled:
        if not log_file:
            # 创建日志目录
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # 生成日志文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = log_dir / f"jianying_downloader_{timestamp}.log"
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    清理文件名，移除非法字符
    
    Args:
        filename: 原始文件名
        max_length: 最大长度
    
    Returns:
        清理后的文件名
    """
    # 移除或替换非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    filename = re.sub(illegal_chars, '_', filename)
    
    # 移除连续的空格和下划线
    filename = re.sub(r'[\s_]+', '_', filename)
    
    # 移除首尾的空格和下划线
    filename = filename.strip(' _')
    
    # 限制长度
    if len(filename) > max_length:
        # 保留文件扩展名
        name, ext = os.path.splitext(filename)
        max_name_length = max_length - len(ext)
        filename = name[:max_name_length] + ext
    
    return filename or "untitled"


def get_file_hash(file_path: str, algorithm: str = "md5") -> str:
    """
    计算文件哈希值
    
    Args:
        file_path: 文件路径
        algorithm: 哈希算法 (md5, sha1, sha256)
    
    Returns:
        文件哈希值
    """
    hash_obj = hashlib.new(algorithm)
    
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except (OSError, IOError):
        return ""


def format_file_size(size: int) -> str:
    """
    格式化文件大小
    
    Args:
        size: 文件大小（字节）
    
    Returns:
        格式化后的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def format_duration(seconds: int) -> str:
    """
    格式化时长
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化后的时长字符串
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def extract_video_info(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    从URL中提取视频信息
    
    Args:
        url: 视频URL
    
    Returns:
        (video_id, resolution) 元组
    """
    try:
        # 尝试从URL中提取视频ID和分辨率信息
        video_id_match = re.search(r'/([a-f0-9]{32})/', url)
        video_id = video_id_match.group(1) if video_id_match else None
        
        resolution_match = re.search(r'_(\d+p)\.', url)
        resolution = resolution_match.group(1) if resolution_match else None
        
        return video_id, resolution
    except Exception:
        return None, None


def create_progress_bar(current: int, total: int, width: int = 50) -> str:
    """
    创建进度条字符串
    
    Args:
        current: 当前进度
        total: 总数
        width: 进度条宽度
    
    Returns:
        进度条字符串
    """
    if total == 0:
        return "█" * width
    
    percentage = min(current / total, 1.0)
    filled_width = int(width * percentage)
    bar = "█" * filled_width + "░" * (width - filled_width)
    
    return f"[{bar}] {percentage:.1%} ({current}/{total})"


def validate_resolution(resolution: str) -> bool:
    """
    验证分辨率格式
    
    Args:
        resolution: 分辨率字符串
    
    Returns:
        是否为有效分辨率
    """
    valid_resolutions = ["1080p", "720p", "480p", "360p", "origin"]
    return resolution in valid_resolutions


def ensure_directory(path: str) -> Path:
    """
    确保目录存在，不存在则创建
    
    Args:
        path: 目录路径
    
    Returns:
        Path对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_safe_path(base_dir: str, filename: str) -> str:
    """
    获取安全的文件路径，防止路径遍历攻击
    
    Args:
        base_dir: 基础目录
        filename: 文件名
    
    Returns:
        安全的完整路径
    """
    # 清理文件名
    clean_filename = sanitize_filename(filename)
    
    # 构建路径
    base_path = Path(base_dir).resolve()
    full_path = (base_path / clean_filename).resolve()
    
    # 检查路径是否在基础目录内
    try:
        full_path.relative_to(base_path)
        return str(full_path)
    except ValueError:
        # 路径遍历攻击，使用安全的默认路径
        return str(base_path / f"safe_{clean_filename}")


def parse_cookie_string(cookie_string: str) -> Dict[str, str]:
    """
    解析Cookie字符串为字典
    
    Args:
        cookie_string: Cookie字符串
    
    Returns:
        Cookie字典
    """
    cookies = {}
    
    if not cookie_string:
        return cookies
    
    try:
        # 分割Cookie项
        for item in cookie_string.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies[key.strip()] = value.strip()
    except Exception as e:
        logging.warning(f"解析Cookie字符串失败: {e}")
    
    return cookies


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔时间
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logging.warning(f"函数 {func.__name__} 第 {attempt + 1} 次尝试失败: {e}")
                        time.sleep(delay)
                    else:
                        logging.error(f"函数 {func.__name__} 在 {max_retries} 次重试后仍然失败")
            
            raise last_exception
        
        return wrapper
    return decorator
