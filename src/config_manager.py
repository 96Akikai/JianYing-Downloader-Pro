#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理器
=========

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

负责管理剪映下载器的所有配置参数
支持从文件加载、环境变量覆盖等功能
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径，默认为 config/settings.json
        """
        self.config_file = config_file or "config/settings.json"
        self.config = self._load_default_config()
        self._load_config_file()
        self._load_env_overrides()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """加载默认配置"""
        return {
            "cookies": {
                # 默认为空，需要用户填写
            },
            "search": {
                "keywords": ["自然风景", "城市夜景"],
                "max_pages": 5,
                "count_per_page": 50,
                "min_duration": 3,
                "max_duration": 300
            },
            "download": {
                "download_dir": "downloads",
                "preferred_resolution": "720p",
                "resolution_priority": ["1080p", "720p", "480p", "360p"],
                "max_workers": 3,
                "max_retries": 3,
                "retry_delay": 2,
                "request_timeout": 30,
                "download_timeout": 300,
                "download_covers": True,
                "save_metadata": True
            },
            "api": {
                "search_url": "https://lv-web-lf.capcut.com/ies/resource/web/v1/effect/search",
                "request_interval": 1,
                "keyword_interval": 2
            },
            "logging": {
                "level": "INFO",
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "file_enabled": True,
                "console_enabled": True
            }
        }
    
    def _load_config_file(self):
        """从文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._merge_config(self.config, file_config)
                logging.info(f"已加载配置文件: {self.config_file}")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logging.warning(f"加载配置文件失败: {e}")
    
    def _load_env_overrides(self):
        """从环境变量加载配置覆盖"""
        env_mappings = {
            "JIANYING_DOWNLOAD_DIR": ["download", "download_dir"],
            "JIANYING_MAX_WORKERS": ["download", "max_workers"],
            "JIANYING_RESOLUTION": ["download", "preferred_resolution"],
            "JIANYING_MAX_PAGES": ["search", "max_pages"],
            "JIANYING_LOG_LEVEL": ["logging", "level"]
        }
        
        for env_var, config_path in env_mappings.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                # 尝试转换数值类型
                if value.isdigit():
                    value = int(value)
                elif value.lower() in ['true', 'false']:
                    value = value.lower() == 'true'
                
                self._set_nested_config(self.config, config_path, value)
                logging.info(f"环境变量覆盖: {env_var} = {value}")
    
    def _merge_config(self, base: Dict, override: Dict):
        """递归合并配置字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_config(base[key], value)
            else:
                base[key] = value
    
    def _set_nested_config(self, config: Dict, path: List[str], value: Any):
        """设置嵌套配置值"""
        current = config
        for key in path[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[path[-1]] = value
    
    def get(self, *keys) -> Any:
        """
        获取配置值
        
        Args:
            keys: 配置键路径，如 'download', 'max_workers'
            
        Returns:
            配置值
        """
        current = self.config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
        return current
    
    def set(self, value: Any, *keys):
        """
        设置配置值
        
        Args:
            value: 要设置的值
            keys: 配置键路径
        """
        self._set_nested_config(self.config, list(keys), value)
    
    def save_config(self, file_path: Optional[str] = None):
        """
        保存配置到文件
        
        Args:
            file_path: 保存路径，默认为当前配置文件路径
        """
        save_path = file_path or self.config_file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
        
        logging.info(f"配置已保存到: {save_path}")
    
    def validate_config(self) -> List[str]:
        """
        验证配置有效性
        
        Returns:
            错误列表，空列表表示配置有效
        """
        errors = []
        
        # 检查必要的Cookie
        if not self.get("cookies"):
            errors.append("未配置Cookie信息")
        
        # 检查下载目录
        download_dir = self.get("download", "download_dir")
        if not download_dir:
            errors.append("未配置下载目录")
        
        # 检查关键词
        keywords = self.get("search", "keywords")
        if not keywords or not isinstance(keywords, list) or len(keywords) == 0:
            errors.append("未配置搜索关键词")
        
        # 检查分辨率
        resolution = self.get("download", "preferred_resolution")
        valid_resolutions = ["1080p", "720p", "480p", "360p", "origin"]
        if resolution not in valid_resolutions:
            errors.append(f"无效的分辨率设置: {resolution}")
        
        # 检查数值范围
        max_workers = self.get("download", "max_workers")
        if not isinstance(max_workers, int) or max_workers < 1 or max_workers > 10:
            errors.append("max_workers 应该在 1-10 之间")
        
        return errors
    
    def get_cookies_dict(self) -> Dict[str, str]:
        """获取Cookie字典"""
        cookies = self.get("cookies") or {}
        return {k: str(v) for k, v in cookies.items()}
    
    def is_cookies_configured(self) -> bool:
        """检查是否已配置Cookie"""
        cookies = self.get_cookies_dict()
        required_cookies = ["sessionid", "sid_tt", "sid_guard"]
        return all(cookie in cookies for cookie in required_cookies)
