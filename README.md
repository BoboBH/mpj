# MPJ - Django Social Media Crawler

一个基于 Django 的社交媒体爬虫项目,支持从多个平台(微博、Social Truth等)爬取博主推文数据。

## 项目结构

```
mpj/
├── mpj/              # Django 项目配置
├── myapp/            # 示例应用
├── crawler/          # 爬虫应用 ⭐
├── .venv/            # 虚拟环境
├── db.sqlite3        # SQLite 数据库
└── manage.py         # Django 管理脚本
```

## 功能特性

- ✅ 多平台支持(微博、Social Truth,可扩展)
- ✅ 自动翻页爬取
- ✅ 双重去重机制(post_id + content_hash)
- ✅ 增量爬取(记录最后爬取位置)
- ✅ Django Admin 管理界面
- ✅ 完整的爬取日志

## 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境 (Windows)
.venv\Scripts\activate

# 激活虚拟环境 (Linux/Mac)
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py migrate
```

### 3. 创建超级用户

```bash
python manage.py createsuperuser
```

### 4. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://127.0.0.1:8000/admin/ 管理数据。

## 使用爬虫

### Python 脚本方式

```python
from crawler.crawler_manager import get_crawler_manager

# 获取管理器
manager = get_crawler_manager()

# 爬取微博博主
result = manager.crawl_blogger(
    platform='weibo',
    blogger_id='1234567890',
    max_pages=5
)

print(f"发现: {result['posts_found']}, 新增: {result['posts_new']}")
```

### Django Shell 方式

```bash
python manage.py shell
```

```python
from crawler.crawler_manager import get_crawler_manager
manager = get_crawler_manager()
result = manager.crawl_blogger('weibo', 'blogger_id')
```

## Git 配置

### 设置 GitHub Token

为了避免每次推送都输入 token,请设置环境变量:

**Windows (CMD):**
```cmd
set GITHUB_TOKEN=ghp_your_token_here
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN="ghp_your_token_here"
```

**Linux/Mac:**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### 使用 Token 推送

```bash
git push https://%GITHUB_TOKEN%@github.com/BoboBH/mpj.git develop
```

或者配置 Git 使用环境变量:
```bash
git config --global credential.helper store
```

## 开发

### 分支策略

- `main` - 生产环境
- `develop` - 开发主分支

### 提交代码

```bash
git add .
git commit -m "your commit message"
git push origin develop
```

## 详细文档

查看 [crawler/README.md](crawler/README.md) 了解爬虫的详细使用方法。

## 许可证

MIT License
