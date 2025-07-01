#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪映素材库下载器核心模块
=======================

Author: Akikai
Motto: Per aspera ad astra (以此苦旅终抵群星)

提供视频搜索、下载、管理等核心功能
"""

import os
import json
import time
import requests
import logging
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import urllib3
from tqdm import tqdm

from .config_manager import ConfigManager
from .utils import (
    sanitize_filename, format_file_size, format_duration,
    ensure_directory, get_safe_path, retry_on_failure,
    create_progress_bar
)


class JianyingDownloader:
    """剪映素材库下载器主类"""
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化下载器
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config = config_manager or ConfigManager()
        self.session = requests.Session()
        self.logger = logging.getLogger("jianying_downloader")
        
        # 禁用SSL警告
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # 设置请求头
        self._setup_session()
        
        # 验证配置
        config_errors = self.config.validate_config()
        if config_errors:
            self.logger.warning(f"配置验证失败: {config_errors}")
    
    def _setup_session(self):
        """设置请求会话"""
        # 设置通用请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Origin': 'https://www.jianying.com',
            'Referer': 'https://www.jianying.com/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        })
        
        # 设置Cookie
        cookies = self.config.get_cookies_dict()
        if cookies:
            self.session.cookies.update(cookies)
            self.logger.info("已设置Cookie信息")
        else:
            self.logger.warning("未配置Cookie信息，可能影响下载功能")
    
    @retry_on_failure(max_retries=3, delay=2.0)
    def search_videos(self, keyword: str, page: int = 1) -> Dict[str, Any]:
        """
        搜索视频
        
        Args:
            keyword: 搜索关键词
            page: 页码
        
        Returns:
            搜索结果字典
        """
        url = self.config.get("api", "search_url")
        count_per_page = self.config.get("search", "count_per_page")
        
        # 构建请求参数
        payload = {
            "keyword": keyword,
            "cursor": (page - 1) * count_per_page,
            "count": count_per_page,
            "search_id": "",
            "category": "",
            "effect_id": "",
            "panel": "default",
            "resource_type": "video",
            "is_commercial": "false",
            "order": 0
        }
        
        try:
            response = self.session.post(
                url, 
                json=payload,
                timeout=self.config.get("download", "request_timeout"),
                verify=False
            )
            response.raise_for_status()
            
            data = response.json()
            if data.get("status_code") == 0:
                self.logger.info(f"搜索关键词 '{keyword}' 第 {page} 页成功")
                return data
            else:
                self.logger.error(f"搜索失败: {data.get('status_msg', '未知错误')}")
                return {}
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"搜索请求失败: {e}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"响应JSON解析失败: {e}")
            raise
    
    def extract_video_info(self, video_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        提取视频信息
        
        Args:
            video_data: 视频数据字典
        
        Returns:
            处理后的视频信息
        """
        try:
            # 基本信息
            video_info = {
                "id": video_data.get("id", ""),
                "title": video_data.get("title", "").strip(),
                "author": video_data.get("author", {}).get("nickname", "未知作者"),
                "duration": video_data.get("duration", 0),
                "create_time": video_data.get("create_time", 0),
                "tags": [tag.get("tag_name", "") for tag in video_data.get("tags", [])],
                "category": video_data.get("category", {}).get("title", ""),
            }
            
            # 下载链接
            video_info["download_urls"] = {}
            videos = video_data.get("videos", {})
            
            for quality, video_url_data in videos.items():
                if video_url_data and isinstance(video_url_data, dict):
                    url_info = video_url_data.get("url_list", [])
                    if url_info and len(url_info) > 0:
                        video_info["download_urls"][quality] = {
                            "url": url_info[0],
                            "size": video_url_data.get("size", 0),
                            "width": video_url_data.get("width", 0),
                            "height": video_url_data.get("height", 0)
                        }
            
            # 封面图片
            cover_urls = video_data.get("cover", {}).get("url_list", [])
            video_info["cover_url"] = cover_urls[0] if cover_urls else ""
            
            # 过滤检查
            duration = video_info["duration"]
            min_duration = self.config.get("search", "min_duration")
            max_duration = self.config.get("search", "max_duration")
            
            if duration < min_duration or duration > max_duration:
                self.logger.debug(f"视频时长 {duration}s 不符合要求，跳过")
                return None
            
            return video_info
            
        except Exception as e:
            self.logger.error(f"提取视频信息失败: {e}")
            return None
    
    def get_best_quality_url(self, download_urls: Dict[str, Any]) -> Optional[Tuple[str, str]]:
        """
        获取最佳质量的下载链接
        
        Args:
            download_urls: 下载链接字典
        
        Returns:
            (url, quality) 元组
        """
        if not download_urls:
            return None
        
        # 获取分辨率优先级
        preferred_resolution = self.config.get("download", "preferred_resolution")
        resolution_priority = self.config.get("download", "resolution_priority")
        
        # 首先尝试首选分辨率
        if preferred_resolution in download_urls:
            url_info = download_urls[preferred_resolution]
            return url_info["url"], preferred_resolution
        
        # 按优先级顺序查找
        for resolution in resolution_priority:
            if resolution in download_urls:
                url_info = download_urls[resolution]
                return url_info["url"], resolution
        
        # 如果都没有，返回第一个可用的
        for quality, url_info in download_urls.items():
            return url_info["url"], quality
        
        return None
    
    @retry_on_failure(max_retries=3, delay=1.0)
    def download_file(self, url: str, file_path: str, description: str = "") -> bool:
        """
        下载文件
        
        Args:
            url: 下载链接
            file_path: 保存路径
            description: 描述信息
        
        Returns:
            下载是否成功
        """
        try:
            # 检查文件是否已存在
            if os.path.exists(file_path):
                self.logger.info(f"文件已存在，跳过下载: {file_path}")
                return True
            
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 开始下载
            timeout = self.config.get("download", "download_timeout")
            response = self.session.get(url, stream=True, timeout=timeout, verify=False)
            response.raise_for_status()
            
            # 获取文件大小
            total_size = int(response.headers.get('content-length', 0))
            
            # 下载文件
            with open(file_path, 'wb') as f:
                if total_size > 0:
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=description or os.path.basename(file_path)
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
            self.logger.info(f"下载完成: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"下载失败 {url}: {e}")
            # 删除不完整的文件
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except:
                    pass
            return False
    
    def download_video(self, video_info: Dict[str, Any], keyword: str) -> bool:
        """
        下载单个视频
        
        Args:
            video_info: 视频信息
            keyword: 关键词（用于分类目录）
        
        Returns:
            下载是否成功
        """
        try:
            # 获取最佳质量下载链接
            best_url_info = self.get_best_quality_url(video_info["download_urls"])
            if not best_url_info:
                self.logger.warning(f"无可用下载链接: {video_info['title']}")
                return False
            
            download_url, quality = best_url_info
            
            # 构建文件名
            title = sanitize_filename(video_info["title"])
            author = sanitize_filename(video_info["author"])
            video_id = video_info["id"]
            filename = f"{title}_{author}_{video_id}_{quality}.mp4"
            
            # 构建保存路径
            download_dir = self.config.get("download", "download_dir")
            keyword_dir = ensure_directory(os.path.join(download_dir, sanitize_filename(keyword)))
            video_path = get_safe_path(str(keyword_dir), filename)
            
            # 下载视频
            success = self.download_file(
                download_url,
                video_path,
                f"视频: {title[:30]}..."
            )
            
            if success:
                # 下载封面（如果启用）
                if self.config.get("download", "download_covers") and video_info.get("cover_url"):
                    cover_filename = f"{title}_{author}_{video_id}_cover.jpg"
                    cover_path = get_safe_path(str(keyword_dir), cover_filename)
                    self.download_file(video_info["cover_url"], cover_path, "封面")
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"下载视频失败: {e}")
            return False
    
    def download_keyword_videos(self, keyword: str, max_pages: Optional[int] = None) -> Dict[str, Any]:
        """
        下载指定关键词的所有视频
        
        Args:
            keyword: 搜索关键词
            max_pages: 最大页数
        
        Returns:
            下载统计信息
        """
        if max_pages is None:
            max_pages = self.config.get("search", "max_pages")
        
        self.logger.info(f"开始下载关键词 '{keyword}' 的视频，最大页数: {max_pages}")
        
        stats = {
            "keyword": keyword,
            "total_found": 0,
            "total_downloaded": 0,
            "failed_downloads": 0,
            "videos": []
        }
        
        # 逐页搜索和下载
        for page in range(1, max_pages + 1):
            try:
                # 搜索视频
                search_result = self.search_videos(keyword, page)
                
                if not search_result:
                    self.logger.warning(f"第 {page} 页搜索结果为空，停止搜索")
                    break
                
                # 解析视频数据
                effects = search_result.get("data", {}).get("effects", [])
                if not effects:
                    self.logger.info(f"第 {page} 页没有更多视频")
                    break
                
                self.logger.info(f"第 {page} 页找到 {len(effects)} 个视频")
                
                # 提取视频信息
                valid_videos = []
                for effect_data in effects:
                    video_info = self.extract_video_info(effect_data)
                    if video_info:
                        valid_videos.append(video_info)
                
                stats["total_found"] += len(valid_videos)
                
                # 并发下载视频
                max_workers = self.config.get("download", "max_workers")
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    # 提交下载任务
                    download_futures = {
                        executor.submit(self.download_video, video_info, keyword): video_info
                        for video_info in valid_videos
                    }
                    
                    # 等待下载完成
                    for future in as_completed(download_futures):
                        video_info = download_futures[future]
                        try:
                            success = future.result()
                            if success:
                                stats["total_downloaded"] += 1
                            else:
                                stats["failed_downloads"] += 1
                            
                            stats["videos"].append({
                                "title": video_info["title"],
                                "author": video_info["author"],
                                "duration": video_info["duration"],
                                "success": success
                            })
                            
                        except Exception as e:
                            self.logger.error(f"下载任务异常: {e}")
                            stats["failed_downloads"] += 1
                
                # 页面间隔
                interval = self.config.get("api", "request_interval")
                if page < max_pages:
                    time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"处理第 {page} 页时出错: {e}")
                continue
        
        self.logger.info(f"关键词 '{keyword}' 下载完成: {stats['total_downloaded']}/{stats['total_found']}")
        return stats
    
    def batch_download(self, keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        批量下载多个关键词的视频
        
        Args:
            keywords: 关键词列表
        
        Returns:
            整体下载统计信息
        """
        if not keywords:
            keywords = self.config.get("search", "keywords")
        
        if not keywords:
            self.logger.error("未指定下载关键词")
            return {}
        
        self.logger.info(f"开始批量下载，关键词数量: {len(keywords)}")
        
        overall_stats = {
            "keywords": keywords,
            "total_keywords": len(keywords),
            "completed_keywords": 0,
            "total_found": 0,
            "total_downloaded": 0,
            "total_failed": 0,
            "keyword_stats": []
        }
        
        # 逐个关键词下载
        for i, keyword in enumerate(keywords, 1):
            self.logger.info(f"处理关键词 {i}/{len(keywords)}: {keyword}")
            
            try:
                keyword_stats = self.download_keyword_videos(keyword)
                overall_stats["keyword_stats"].append(keyword_stats)
                overall_stats["total_found"] += keyword_stats["total_found"]
                overall_stats["total_downloaded"] += keyword_stats["total_downloaded"]
                overall_stats["total_failed"] += keyword_stats["failed_downloads"]
                overall_stats["completed_keywords"] += 1
                
                # 关键词间隔
                if i < len(keywords):
                    interval = self.config.get("api", "keyword_interval")
                    time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"处理关键词 '{keyword}' 时出错: {e}")
                continue
        
        # 保存统计报告
        if self.config.get("download", "save_metadata"):
            self.save_download_report(overall_stats)
        
        self.logger.info(f"批量下载完成: {overall_stats['total_downloaded']}/{overall_stats['total_found']}")
        return overall_stats
    
    def save_download_report(self, stats: Dict[str, Any]):
        """
        保存下载报告
        
        Args:
            stats: 统计信息
        """
        try:
            download_dir = self.config.get("download", "download_dir")
            report_dir = ensure_directory(os.path.join(download_dir, "reports"))
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            report_file = report_dir / f"download_report_{timestamp}.json"
            
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"下载报告已保存: {report_file}")
            
        except Exception as e:
            self.logger.error(f"保存下载报告失败: {e}")
    
    def get_download_status(self) -> Dict[str, Any]:
        """
        获取下载状态统计
        
        Returns:
            下载状态信息
        """
        download_dir = Path(self.config.get("download", "download_dir"))
        
        if not download_dir.exists():
            return {"status": "未开始下载"}
        
        # 统计各关键词目录的文件数量
        keyword_stats = {}
        total_files = 0
        total_size = 0
        
        for keyword_dir in download_dir.iterdir():
            if keyword_dir.is_dir() and keyword_dir.name != "reports":
                video_files = list(keyword_dir.glob("*.mp4"))
                cover_files = list(keyword_dir.glob("*_cover.jpg"))
                
                keyword_stats[keyword_dir.name] = {
                    "videos": len(video_files),
                    "covers": len(cover_files),
                    "total_files": len(video_files) + len(cover_files)
                }
                
                total_files += len(video_files) + len(cover_files)
                
                # 计算总大小
                for file_path in keyword_dir.iterdir():
                    if file_path.is_file():
                        total_size += file_path.stat().st_size
        
        return {
            "status": "已有下载",
            "total_files": total_files,
            "total_size": format_file_size(total_size),
            "keyword_stats": keyword_stats,
            "download_dir": str(download_dir)
        }
