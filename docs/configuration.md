# 🔧 配置指南

本文档详细介绍如何配置剪映素材库下载器Pro。

## 📋 目录

1. [Cookie配置](#cookie配置)
2. [搜索配置](#搜索配置)
3. [下载配置](#下载配置)
4. [API配置](#api配置)
5. [日志配置](#日志配置)
6. [环境变量](#环境变量)
7. [配置验证](#配置验证)

## 🍪 Cookie配置

### 重要性
Cookie是访问剪映素材库的关键认证信息，没有正确的Cookie将无法下载视频。

### 获取方法

#### 步骤1: 访问剪映网站
```
https://www.jianying.com
```

#### 步骤2: 登录账号
- 使用您的剪映账号登录
- 确保账号有素材库访问权限

#### 步骤3: 打开开发者工具
- Windows/Linux: 按 `F12`
- Mac: 按 `Cmd + Option + I`
- 或右键选择"检查"/"检查元素"

#### 步骤4: 定位网络请求
1. 切换到 `Network` (网络) 标签
2. 在剪映网站上搜索任意关键词（如"风景"）
3. 找到名为 `search` 的请求（通常是POST请求）
4. 点击该请求查看详情

#### 步骤5: 复制Cookie
1. 在右侧面板找到 `Request Headers`
2. 找到 `Cookie:` 行
3. 复制整个Cookie值

### 配置格式

将获取到的Cookie信息填入 `config/settings.json`:

```json
{
  "cookies": {
    "sessionid": "从Cookie中提取的sessionid值",
    "sid_tt": "从Cookie中提取的sid_tt值",
    "sid_guard": "从Cookie中提取的sid_guard值",
    "其他项": "对应的值"
  }
}
```

### 关键Cookie项

| 项目 | 必需性 | 说明 |
|------|--------|------|
| `sessionid` | ✅ 必需 | 会话标识符 |
| `sid_tt` | ✅ 必需 | 用户令牌 |
| `sid_guard` | ✅ 必需 | 安全令牌 |
| `uid_tt` | 🔶 推荐 | 用户ID |
| `passport_csrf_token` | 🔶 推荐 | CSRF保护令牌 |

### Cookie更新

- **更新频率**: 建议每周检查一次
- **失效症状**: 搜索无结果、下载失败
- **更新方法**: 重复上述获取步骤

## 🔍 搜索配置

### 基本设置

```json
{
  "search": {
    "keywords": ["风景", "城市", "自然"],
    "max_pages": 5,
    "count_per_page": 50,
    "min_duration": 3,
    "max_duration": 300
  }
}
```

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `keywords` | 数组 | `[]` | 搜索关键词列表 |
| `max_pages` | 整数 | `5` | 每个关键词最大搜索页数 |
| `count_per_page` | 整数 | `50` | 每页返回的视频数量 |
| `min_duration` | 整数 | `3` | 最小视频时长（秒） |
| `max_duration` | 整数 | `300` | 最大视频时长（秒） |

### 关键词策略

#### 有效关键词示例
```json
{
  "keywords": [
    "秋天风景",      // 季节+场景
    "城市夜景",      // 地点+时间
    "海边日落",      // 地点+现象
    "花朵特写",      // 对象+视角
    "山水画面",      // 风格+内容
    "人物剪影",      // 主体+效果
    "延时摄影",      // 技术+类型
    "航拍镜头"       // 技术+视角
  ]
}
```

#### 避免的关键词
- 过于泛泛的词：如"视频"、"素材"
- 英文关键词：系统主要支持中文
- 特殊字符：避免使用符号和数字

### 时长过滤

```json
{
  "min_duration": 5,    // 过滤掉5秒以下的短视频
  "max_duration": 180   // 过滤掉3分钟以上的长视频
}
```

## 📥 下载配置

### 完整配置

```json
{
  "download": {
    "download_dir": "downloads",
    "preferred_resolution": "720p",
    "resolution_priority": ["1080p", "720p", "480p", "360p"],
    "max_workers": 3,
    "max_retries": 3,
    "retry_delay": 2,
    "request_timeout": 30,
    "download_timeout": 300,
    "download_covers": true,
    "save_metadata": true
  }
}
```

### 分辨率设置

#### 可用分辨率
| 分辨率 | 尺寸 | 文件大小 | 推荐场景 |
|--------|------|----------|----------|
| `1080p` | 1920x1080 | 大 | 高质量需求 |
| `720p` | 1280x720 | 中等 | 一般使用 ✅ |
| `480p` | 854x480 | 较小 | 网络较慢 |
| `360p` | 640x360 | 小 | 存储受限 |
| `origin` | 原始 | 最大 | 专业用途 |

#### 智能选择策略
1. 首先尝试 `preferred_resolution`
2. 如果不可用，按 `resolution_priority` 顺序选择
3. 自动跳过不可用的分辨率

### 并发控制

#### 推荐设置
```json
{
  "max_workers": 3,        // 并发下载数
  "request_timeout": 30,   // 请求超时时间
  "download_timeout": 300  // 下载超时时间
}
```

#### 性能调优

| 网络状况 | max_workers | timeout | 说明 |
|----------|-------------|---------|------|
| 优秀 | 5-8 | 30/300 | 高速网络 |
| 良好 | 3-5 | 30/300 | 家庭宽带 ✅ |
| 一般 | 2-3 | 60/600 | 移动网络 |
| 较差 | 1-2 | 120/1200 | 慢速网络 |

### 重试机制

```json
{
  "max_retries": 3,    // 最大重试次数
  "retry_delay": 2     // 重试间隔（秒）
}
```

### 文件管理

```json
{
  "download_covers": true,    // 下载视频封面图片
  "save_metadata": true       // 保存视频元数据信息
}
```

## 🌐 API配置

### 基本设置

```json
{
  "api": {
    "search_url": "https://lv-web-lf.capcut.com/ies/resource/web/v1/effect/search",
    "request_interval": 1,
    "keyword_interval": 2
  }
}
```

### 频率控制

| 参数 | 说明 | 推荐值 |
|------|------|--------|
| `request_interval` | 页面请求间隔 | 1-2秒 |
| `keyword_interval` | 关键词间隔 | 2-5秒 |

### 礼貌爬取原则

- 避免过高的请求频率
- 遵守网站的robots.txt
- 监控服务器响应，及时调整策略

## 📝 日志配置

### 完整配置

```json
{
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_enabled": true,
    "console_enabled": true
  }
}
```

### 日志级别

| 级别 | 说明 | 使用场景 |
|------|------|----------|
| `DEBUG` | 详细调试信息 | 开发调试 |
| `INFO` | 一般信息 | 正常使用 ✅ |
| `WARNING` | 警告信息 | 监控异常 |
| `ERROR` | 错误信息 | 问题排查 |

### 日志输出

```json
{
  "file_enabled": true,      // 保存到文件
  "console_enabled": true    // 控制台输出
}
```

## 🌍 环境变量

### 支持的环境变量

```bash
# 下载配置
export JIANYING_DOWNLOAD_DIR="./my_downloads"
export JIANYING_MAX_WORKERS="5"
export JIANYING_RESOLUTION="1080p"

# 搜索配置  
export JIANYING_MAX_PAGES="10"

# 日志配置
export JIANYING_LOG_LEVEL="DEBUG"
```

### Windows设置

```batch
set JIANYING_DOWNLOAD_DIR=D:\Downloads
set JIANYING_MAX_WORKERS=5
set JIANYING_RESOLUTION=1080p
```

### Linux/Mac设置

```bash
# 临时设置
export JIANYING_DOWNLOAD_DIR="/home/user/downloads"

# 永久设置（添加到 .bashrc 或 .zshrc）
echo 'export JIANYING_DOWNLOAD_DIR="/home/user/downloads"' >> ~/.bashrc
```

## ✅ 配置验证

### 自动验证

程序启动时会自动验证配置：

- ✅ Cookie完整性检查
- ✅ 下载目录权限验证
- ✅ 分辨率格式检查
- ✅ 数值范围验证

### 手动验证

#### 检查Cookie有效性

```python
from src import ConfigManager

config = ConfigManager()
if config.is_cookies_configured():
    print("✅ Cookie配置正确")
else:
    print("❌ Cookie配置错误")
```

#### 验证配置文件

```python
config = ConfigManager()
errors = config.validate_config()
if errors:
    print("❌ 配置错误:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ 配置验证通过")
```

## 📚 配置示例

### 最小配置

```json
{
  "cookies": {
    "sessionid": "your_sessionid",
    "sid_tt": "your_sid_tt",
    "sid_guard": "your_sid_guard"
  },
  "search": {
    "keywords": ["风景"]
  }
}
```

### 完整配置

```json
{
  "cookies": {
    "sessionid": "90e31d4304c08d095b4862f28d2530f3",
    "sid_tt": "90e31d4304c08d095b4862f28d2530f3",
    "sid_guard": "90e31d4304c08d095b4862f28d2530f3%7C1750752897%7C5184000%7CSat%2C+23-Aug-2025+08%3A14%3A57+GMT",
    "uid_tt": "a86eba08ed6672e8b322ab33645dd3b6",
    "passport_csrf_token": "ad45dd0974421cb8d4af71c3a3a4ac63"
  },
  "search": {
    "keywords": [
      "秋天风景", "城市夜景", "海边日落", 
      "山水风景", "花朵特写", "自然风光"
    ],
    "max_pages": 5,
    "count_per_page": 50,
    "min_duration": 5,
    "max_duration": 180
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
    "download_covers": true,
    "save_metadata": true
  },
  "api": {
    "search_url": "https://lv-web-lf.capcut.com/ies/resource/web/v1/effect/search",
    "request_interval": 1,
    "keyword_interval": 2
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_enabled": true,
    "console_enabled": true
  }
}
```

## 🔧 配置技巧

### 1. 性能优化

```json
{
  "download": {
    "max_workers": 2,           // 降低并发避免被限制
    "preferred_resolution": "480p",  // 选择较低分辨率提高速度
    "download_covers": false    // 关闭封面下载节省时间
  }
}
```

### 2. 高质量下载

```json
{
  "download": {
    "preferred_resolution": "1080p",
    "download_covers": true,
    "save_metadata": true
  },
  "search": {
    "min_duration": 10,         // 只要较长的视频
    "max_duration": 60          // 避免过长视频
  }
}
```

### 3. 批量采集

```json
{
  "search": {
    "max_pages": 10,            // 增加搜索页数
    "count_per_page": 50        // 每页最大数量
  },
  "api": {
    "request_interval": 2,      // 增加间隔避免限制
    "keyword_interval": 5
  }
}
```

## 🚨 常见配置错误

### 1. JSON格式错误

❌ **错误示例**:
```json
{
  "cookies": {
    "sessionid": "value",    // 缺少引号
  }                         // 多余的逗号
}
```

✅ **正确示例**:
```json
{
  "cookies": {
    "sessionid": "value"
  }
}
```

### 2. Cookie格式错误

❌ **错误**: 直接粘贴整个Cookie字符串
✅ **正确**: 解析为键值对格式

### 3. 路径配置错误

❌ **错误**: 使用反斜杠 `"download_dir": "C:\downloads"`
✅ **正确**: 使用正斜杠 `"download_dir": "C:/downloads"`

### 4. 数值类型错误

❌ **错误**: `"max_workers": "3"` (字符串)
✅ **正确**: `"max_workers": 3` (数字)

---

需要更多帮助？请查看 [README.md](README.md) 或提交 Issue。
