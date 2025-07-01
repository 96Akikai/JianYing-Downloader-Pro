# 🚀 安装指南

本文档提供详细的安装步骤和环境配置说明。

## 📋 系统要求

### 操作系统
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 18.04+, CentOS 7+)

### Python版本
- ✅ Python 3.7+
- ✅ Python 3.8+ (推荐)
- ✅ Python 3.9+
- ✅ Python 3.10+
- ✅ Python 3.11+

### 硬件要求
- **CPU**: 双核或更高
- **内存**: 4GB RAM (推荐8GB+)
- **存储**: 10GB+ 可用空间
- **网络**: 稳定的互联网连接

## 📦 安装方法

### 方法一: 一键安装 (推荐)

#### Windows用户
```batch
# 1. 下载项目
git clone https://github.com/your-repo/jianying_downloader_pro.git
cd jianying_downloader_pro

# 2. 运行一键安装脚本
scripts\install.bat
```

#### Linux/Mac用户
```bash
# 1. 下载项目
git clone https://github.com/your-repo/jianying_downloader_pro.git
cd jianying_downloader_pro

# 2. 设置脚本权限并运行
chmod +x scripts/install.sh
./scripts/install.sh
```

### 方法二: 手动安装

#### 步骤1: 检查Python环境

**Windows:**
```batch
python --version
```

**Linux/Mac:**
```bash
python3 --version
```

#### 步骤2: 下载项目

**使用Git:**
```bash
git clone https://github.com/your-repo/jianying_downloader_pro.git
cd jianying_downloader_pro
```

**手动下载:**
1. 下载项目ZIP文件
2. 解压到目标目录
3. 进入项目目录

#### 步骤3: 创建虚拟环境 (推荐)

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 步骤4: 安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤5: 创建配置目录

```bash
# 确保配置目录存在
mkdir -p config downloads logs
```

## 🔧 环境配置

### Python环境管理

#### 使用Anaconda (推荐)

```bash
# 创建环境
conda create -n jianying python=3.9
conda activate jianying

# 安装依赖
pip install -r requirements.txt
```

#### 使用pyenv

```bash
# 安装Python版本
pyenv install 3.9.10
pyenv local 3.9.10

# 创建虚拟环境
python -m venv venv
source venv/bin/activate
```

### 依赖包说明

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| `requests` | >=2.28.0 | HTTP请求处理 |
| `urllib3` | >=1.26.0 | URL处理和连接池 |
| `tqdm` | >=4.64.0 | 进度条显示 |
| `pathlib` | >=1.0.1 | 路径处理 |

### 可选依赖

```bash
# 彩色终端输出 (Windows)
pip install colorama

# 更快的JSON解析
pip install orjson

# 异步支持
pip install aiohttp
```

## 🔍 安装验证

### 基本验证

```bash
# 检查Python版本
python --version

# 检查依赖包
pip list

# 运行程序检查
python main.py --help
```

### 详细测试

创建测试脚本 `test_installation.py`:

```python
#!/usr/bin/env python3

import sys
import importlib.util

def test_python_version():
    """测试Python版本"""
    if sys.version_info >= (3, 7):
        print("✅ Python版本符合要求")
        return True
    else:
        print("❌ Python版本过低，需要3.7+")
        return False

def test_dependencies():
    """测试依赖包"""
    required_packages = {
        'requests': 'HTTP请求库',
        'urllib3': 'URL处理库', 
        'tqdm': '进度条库',
        'pathlib': '路径处理库'
    }
    
    success = True
    for package, description in required_packages.items():
        try:
            importlib.import_module(package)
            print(f"✅ {package} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (未安装)")
            success = False
    
    return success

def test_config_files():
    """测试配置文件"""
    import os
    
    required_dirs = ['config', 'downloads', 'logs']
    success = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ 目录 {dir_name} 存在")
        else:
            print(f"⚠️  目录 {dir_name} 不存在，将自动创建")
            os.makedirs(dir_name, exist_ok=True)
    
    return success

def main():
    """主测试函数"""
    print("🔍 开始安装验证...")
    print("=" * 50)
    
    tests = [
        ("Python版本", test_python_version),
        ("依赖包", test_dependencies),
        ("配置文件", test_config_files)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！安装成功！")
    else:
        print("❌ 部分测试失败，请检查安装")

if __name__ == "__main__":
    main()
```

运行测试:
```bash
python test_installation.py
```

## 🚨 常见安装问题

### 问题1: Python未找到

**错误信息**: `'python' is not recognized as an internal or external command`

**解决方案**:
1. 确认Python已正确安装
2. 检查环境变量PATH设置
3. 尝试使用 `python3` 命令

**Windows安装Python**:
1. 访问 https://www.python.org/downloads/
2. 下载最新版Python
3. 安装时勾选"Add Python to PATH"

### 问题2: pip安装失败

**错误信息**: `Could not install packages due to an EnvironmentError`

**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 如果权限问题，使用用户安装
pip install --user -r requirements.txt
```

### 问题3: SSL证书错误

**错误信息**: `SSL: CERTIFICATE_VERIFY_FAILED`

**解决方案**:
```bash
# 临时跳过SSL验证
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

# 或升级证书
pip install --upgrade certifi
```

### 问题4: 虚拟环境激活失败

**Windows PowerShell权限问题**:
```powershell
# 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后激活虚拟环境
venv\Scripts\Activate.ps1
```

### 问题5: 依赖版本冲突

**解决方案**:
```bash
# 创建全新虚拟环境
python -m venv fresh_env
source fresh_env/bin/activate  # Linux/Mac
# 或
fresh_env\Scripts\activate     # Windows

# 重新安装依赖
pip install -r requirements.txt
```

## 🔄 更新指南

### 检查更新

```bash
# 拉取最新代码
git pull origin main

# 检查依赖更新
pip list --outdated
```

### 更新依赖

```bash
# 更新所有包
pip install --upgrade -r requirements.txt

# 更新单个包
pip install --upgrade requests
```

### 备份配置

更新前备份重要配置:
```bash
# 备份配置文件
cp config/settings.json config/settings.json.backup

# 备份下载数据
cp -r downloads downloads_backup
```

## 🌐 代理配置

### HTTP代理

```bash
# 设置环境变量
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# pip代理设置
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

### 程序内代理

在 `config/settings.json` 中添加:
```json
{
  "proxy": {
    "enabled": true,
    "http": "http://proxy.company.com:8080",
    "https": "http://proxy.company.com:8080"
  }
}
```

## 📱 Docker安装

### 构建镜像

创建 `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

### 运行容器

```bash
# 构建镜像
docker build -t jianying-downloader .

# 运行容器
docker run -it -v $(pwd)/downloads:/app/downloads jianying-downloader
```

## 💻 IDE配置

### VS Code配置

创建 `.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

### PyCharm配置

1. 打开项目目录
2. 设置Python解释器: File → Settings → Project → Python Interpreter
3. 选择虚拟环境中的Python

## 🔧 开发环境配置

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

创建 `requirements-dev.txt`:
```
# 开发依赖
black>=22.0.0
flake8>=4.0.0
pytest>=7.0.0
pytest-cov>=3.0.0
mypy>=0.910
```

### 代码格式化

```bash
# 使用black格式化
black src/

# 检查代码风格
flake8 src/

# 类型检查
mypy src/
```

## 📞 获取帮助

如果安装过程中遇到问题:

1. **查看日志**: 检查 `logs/` 目录下的错误日志
2. **搜索文档**: 查看本项目的其他文档文件
3. **提交Issue**: 在GitHub上描述具体问题
4. **社区支持**: 加入相关技术交流群

---

**下一步**: 查看 [配置指南](configuration.md) 了解如何配置程序。
