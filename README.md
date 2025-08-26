# 🎬 剪映素材库下载器 Pro

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen.svg)]()

一个功能完整、生产级的剪映素材库下载工具，支持智能搜索、批量下载、多分辨率选择、断点续传等专业功能。

## ✨ 主要特性

### 🔍 智能搜索
- 🎯 支持中文关键词精确搜索
- 📄 支持多页搜索结果获取
- 🏷️ 支持按分类、时长等条件过滤
- 🔄 智能去重和内容筛选

### 📥 强大下载
- ⚡ 多线程并发下载，提升效率
- 🎭 多分辨率自动选择 (1080p/720p/480p/360p)
- 🔄 断点续传，支持下载中断恢复
- 📁 智能文件命名和分类存储
- 🖼️ 可选下载视频封面图片

### ⚙️ 灵活配置
- 📝 JSON配置文件，易于管理
- 🌍 环境变量支持，适合部署
- 🎚️ 可调整并发数、超时时间等参数
- 📊 完整的下载日志和统计报告

### 🛡️ 安全可靠
- 🔒 安全的文件路径处理
- 🔄 智能重试机制
- 📋 完整的错误处理和日志记录
- 🚫 防止重复下载

## 📁 项目结构

```
jianying_downloader_pro/
├── main.py                 # 主启动脚本
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明文档
├── LICENSE                # 许可证文件
├── src/                   # 源代码目录
│   ├── __init__.py        # 包初始化文件
│   ├── downloader.py      # 核心下载器类
│   ├── config_manager.py  # 配置管理器
│   └── utils.py           # 工具函数模块
├── config/                # 配置文件目录
│   └── settings.json      # 主配置文件
├── docs/                  # 文档目录
│   ├── installation.md    # 安装指南
│   ├── configuration.md   # 配置指南
│   └── api.md             # API文档
├── scripts/               # 脚本目录
│   ├── install.bat        # Windows一键安装
│   └── install.sh         # Linux/Mac一键安装
├── downloads/             # 默认下载目录 (自动创建)
├── logs/                  # 日志文件目录 (自动创建)
└── reports/               # 下载报告目录 (自动创建)
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.7 或更高版本
- 稳定的网络连接
- 足够的存储空间

### 2. 安装依赖

```bash
# 克隆或下载项目
cd jianying_downloader_pro

# 安装依赖包
pip install -r requirements.txt
```

### 3. 配置Cookie

这是最重要的步骤！请按照以下步骤获取Cookie：

#### 步骤A：获取Cookie信息

1. **打开剪映网页版**
   - 访问 (https://www.jianying.com/ai-creator/storyboard/22781143298?workspaceId=7373574164885749814&spaceId=7350593388275564836&draftId=DE64EF91-88B4-4A0B-A960-B6E09A557641)
   - 登录您的账号

2. **打开开发者工具**
   - 按 `F12` 或右键选择"检查"
   - 切换到 `Network` (网络) 标签

3. **执行搜索操作**
   - 在剪映网站上搜索任意关键词（如"风景"）
   - 在Network标签中找到名为 `search` 的请求

4. **复制Cookie信息**
   - 点击该请求，在右侧找到 `Request Headers`
   - 找到 `Cookie:` 行，复制整个Cookie值

#### 步骤B：配置Cookie文件

编辑 `config/settings.json` 文件：

```json
{
  "cookies": {
    "sessionid": "您的sessionid值",
    "sid_tt": "您的sid_tt值", 
    "sid_guard": "您的sid_guard值",
    "其他cookie项": "对应的值"
  }
}
```

**重要的Cookie项：**
- `sessionid` - 会话ID（必需）
- `sid_tt` - 用户令牌（必需）
- `sid_guard` - 安全令牌（必需）
- 其他项目可选，但建议都填写以提高成功率

### 4. 运行程序

你可以选择喜欢的界面风格：

#### 方案一: 使用UI选择器 (推荐)
```bash
python launcher.py
```
然后选择你喜欢的界面风格：
- **标准版** - 现代美观，使用彩色和图标
- **简洁版** - 简洁现代，适中装饰
- **极简版** - 纯文本，最高兼容性

#### 方案二: 直接启动
```bash
# 标准版 (推荐)
python main.py

# 简洁版
python main_simple.py

# 极简版 (兼容性最好)
python main_minimal.py
```

#### 方案三: 一键启动 (Windows)
```bash
# 双击启动
start.bat
```

## ⚙️ 详细配置

### 配置文件说明 (`config/settings.json`)

```json
{
  "cookies": {
    // Cookie配置 - 从浏览器开发者工具获取
    "sessionid": "必需 - 会话ID",
    "sid_tt": "必需 - 用户令牌", 
    "sid_guard": "必需 - 安全令牌"
  },
  "search": {
    "keywords": ["风景", "城市"],     // 搜索关键词列表
    "max_pages": 5,                  // 每个关键词最大搜索页数
    "count_per_page": 50,            // 每页视频数量
    "min_duration": 3,               // 最小视频时长(秒)
    "max_duration": 300              // 最大视频时长(秒)
  },
  "download": {
    "download_dir": "downloads",     // 下载目录
    "preferred_resolution": "720p",  // 首选分辨率
    "resolution_priority": [         // 分辨率优先级
      "1080p", "720p", "480p", "360p"
    ],
    "max_workers": 3,                // 并发下载数
    "max_retries": 3,                // 最大重试次数
    "retry_delay": 2,                // 重试间隔(秒)
    "request_timeout": 30,           // 请求超时(秒)
    "download_timeout": 300,         // 下载超时(秒)
    "download_covers": true,         // 是否下载封面
    "save_metadata": true            // 是否保存元数据
  },
  "api": {
    "search_url": "API地址",         // 搜索API URL
    "request_interval": 1,           // 请求间隔(秒)
    "keyword_interval": 2            // 关键词间隔(秒)
  },
  "logging": {
    "level": "INFO",                 // 日志级别
    "file_enabled": true,            // 启用文件日志
    "console_enabled": true          // 启用控制台日志
  }
}
```

### 环境变量配置

您也可以使用环境变量覆盖配置：

```bash
export JIANYING_DOWNLOAD_DIR="./my_downloads"
export JIANYING_MAX_WORKERS="5"
export JIANYING_RESOLUTION="1080p"
export JIANYING_MAX_PAGES="10"
export JIANYING_LOG_LEVEL="DEBUG"
```

## 🎯 使用方法

### 交互式使用

运行程序后，选择对应的功能：

```
📋 下载选项
1. 单个关键词下载    - 下载单个关键词的视频
2. 批量关键词下载    - 下载多个关键词的视频  
3. 自定义配置下载    - 临时修改配置并下载
4. 查看下载状态      - 查看已下载的文件统计
0. 退出
```

### 编程接口使用

```python
from src import JianyingDownloader, ConfigManager

# 创建配置管理器
config = ConfigManager("config/settings.json")

# 创建下载器
downloader = JianyingDownloader(config)

# 下载单个关键词
stats = downloader.download_keyword_videos("自然风景", max_pages=3)

# 批量下载
keywords = ["风景", "城市夜景", "海边日落"]
overall_stats = downloader.batch_download(keywords)

# 查看下载状态
status = downloader.get_download_status()
print(f"总文件数: {status['total_files']}")
```

## 📊 输出文件

### 视频文件
- **命名格式**: `标题_作者_视频ID_分辨率.mp4`
- **存储位置**: `downloads/关键词/`
- **示例**: `秋天枫叶_张三_abc123_720p.mp4`

### 封面图片  
- **命名格式**: `标题_作者_视频ID_cover.jpg`
- **存储位置**: `downloads/关键词/`
- **示例**: `秋天枫叶_张三_abc123_cover.jpg`

### 下载报告
- **文件位置**: `downloads/reports/`
- **文件格式**: JSON
- **包含信息**: 下载统计、成功率、失败原因等

### 日志文件
- **文件位置**: `logs/`
- **文件格式**: 文本日志
- **内容**: 详细的运行日志和错误信息

## 🔧 高级功能

### 1. 分辨率选择策略

程序会按照优先级自动选择最佳分辨率：

1. **首选分辨率**: 配置中的 `preferred_resolution`
2. **优先级顺序**: 按 `resolution_priority` 数组顺序
3. **自动降级**: 如果首选不可用，自动选择次优选项
4. **智能选择**: 考虑文件大小和网络状况

### 2. 并发下载控制

```json
{
  "download": {
    "max_workers": 3,        // 建议值: 2-5
    "request_timeout": 30,   // 网络较差时增加
    "download_timeout": 300  // 大文件下载时增加
  }
}
```

### 3. 文件名自定义

程序自动清理文件名中的非法字符：
- 移除: `< > : " / \ | ? *`
- 替换连续空格为下划线
- 限制总长度防止路径过长

### 4. 下载去重

- **文件级去重**: 检查文件是否已存在
- **内容级去重**: 基于视频ID避免重复
- **智能跳过**: 已下载的文件自动跳过

## 🚨 常见问题

### Q1: Cookie获取失败或失效

**问题**: 无法获取Cookie或Cookie已过期
**解决方案**:
1. 确保在剪映官网已登录
2. 重新按步骤获取Cookie
3. 检查Cookie格式是否正确
4. 定期更新Cookie（建议每周更新）

### Q2: 下载速度慢

**问题**: 下载速度很慢或经常超时
**解决方案**:
1. 减少并发数 `max_workers`
2. 增加超时时间 `download_timeout`
3. 选择较低分辨率
4. 检查网络连接质量

### Q3: 某些视频下载失败

**问题**: 部分视频下载失败
**可能原因**:
- 视频链接已过期
- 网络连接问题  
- 视频已被删除
- Cookie权限不足

**解决方案**:
1. 查看详细日志了解失败原因
2. 更新Cookie信息
3. 重新运行下载程序
4. 跳过失败的视频继续下载

### Q4: 程序运行异常

**问题**: 程序崩溃或异常退出
**解决方案**:
1. 检查Python版本 (需要3.7+)
2. 确认所有依赖已正确安装
3. 查看日志文件了解错误详情
4. 检查磁盘空间是否充足

### Q5: 配置文件错误

**问题**: 配置文件格式错误
**解决方案**:
1. 确保JSON格式正确
2. 检查是否有语法错误（如缺少逗号、引号）
3. 使用JSON验证工具检查格式
4. 参考提供的模板文件

## 📈 性能优化

### 网络优化
```json
{
  "download": {
    "max_workers": 3,           // 根据网络调整
    "request_timeout": 30,      // 网络差时增加
    "retry_delay": 2            // 重试间隔
  },
  "api": {
    "request_interval": 1,      // 请求间隔
    "keyword_interval": 2       // 关键词间隔
  }
}
```

### 存储优化
- 选择SSD硬盘提升写入速度
- 确保足够的剩余空间
- 定期清理临时文件

### 内存优化
- 减少并发数降低内存占用
- 大批量下载时分批处理
- 监控系统资源使用情况

## 📜 许可证

本项目采用 MIT 许可证，详情请查看 [LICENSE](LICENSE) 文件。

## ⚠️ 使用声明

1. **合规使用**: 请遵守剪映网站的使用条款和相关法律法规
2. **个人学习**: 本工具仅供学习研究使用，请勿用于商业用途
3. **尊重版权**: 下载的内容请尊重原作者版权
4. **适度使用**: 请合理控制下载频率，避免对服务器造成过大压力

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进项目！

### 贡献指南
1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📞 支持

如果您在使用过程中遇到问题，请：

1. 查看本文档的常见问题部分
2. 检查 `logs/` 目录下的日志文件
3. 在 GitHub 上提交 Issue
4. 详细描述问题和错误日志

---

**作者**: Akikai  
**版本**: 2.0.0  
**更新日期**: 2025年6月30日
