# 社交媒体爬虫应用

这是一个可扩展的社交媒体爬虫框架,支持从多个平台(微博、Social Truth等)爬取博主推文数据。

## 功能特性

- ✅ **基类设计**: 提供统一的爬虫基类,易于扩展新平台
- ✅ **翻页爬取**: 支持自动翻页爬取博主所有推文
- ✅ **自动去重**: 基于 `post_id` 和 `content_hash` 双重去重机制
- ✅ **增量爬取**: 记录最后爬取时间,支持增量更新
- ✅ **数据管理**: Django Admin 后台管理界面
- ✅ **爬虫日志**: 完整的爬取日志记录

## 项目结构

```
crawler/
├── __init__.py
├── models.py                 # 数据模型
├── admin.py                  # Admin 管理界面
├── base_crawler.py           # 爬虫基类
├── weibo_crawler.py          # 微博爬虫实现
├── social_truth_crawler.py   # Social Truth 爬虫实现
├── crawler_manager.py        # 爬虫管理器
├── config.py                 # 配置文件
├── migrations/               # 数据库迁移
└── README.md                 # 本文档
```

## 数据模型

### Blogger (博主)
- 平台、博主ID、用户名、昵称
- 头像、主页、简介
- 粉丝数、关注数、推文数
- 最后爬取时间、最后推文ID/时间

### Post (推文)
- 关联博主、平台、推文ID
- 内容、原始数据(JSON)
- 图片、视频、外部链接
- 点赞、评论、转发数
- 发布时间、爬取时间
- 转发信息、内容哈希

### CrawlerLog (爬虫日志)
- 平台、博主、状态
- 发现/新增/重复推文数
- 开始/结束时间、耗时
- 错误信息

## 快速开始

### 1. 使用管理器爬取数据

```python
from crawler.crawler_manager import get_crawler_manager

# 获取管理器实例
manager = get_crawler_manager()

# 爬取单个博主
result = manager.crawl_blogger(
    platform='weibo',
    blogger_id='1234567890',
    max_pages=5
)

print(f"成功: {result['success']}")
print(f"发现: {result['posts_found']}, 新增: {result['posts_new']}")
```

### 2. 批量爬取多个博主

```python
# 批量爬取
results = manager.crawl_multiple_bloggers(
    platform='weibo',
    blogger_ids=['123456', '789012', '345678'],
    max_pages=3
)

for result in results:
    print(f"{result['blogger_id']}: 新增 {result['posts_new']} 条")
```

### 3. 直接使用爬虫类

```python
from crawler.weibo_crawler import WeiboCrawler

# 创建爬虫实例
crawler = WeiboCrawler(max_pages=10, delay=2.0)

# 爬取博主
result = crawler.crawl_blogger('bobo123')
```

### 4. 使用带认证的 API 爬虫

```python
from crawler.weibo_crawler import WeiboAPICrawler

# 需要先在微博开放平台申请 access_token
crawler = WeiboAPICrawler(
    access_token='your_access_token_here',
    max_pages=10
)

result = crawler.crawl_blogger('1234567890')
```

## 扩展新平台

### 步骤 1: 创建爬虫类

```python
from crawler.base_crawler import BaseCrawler
from crawler.models import SocialMediaPlatform

class MyPlatformCrawler(BaseCrawler):
    platform = 'my_platform'  # 平台标识
    platform_name = '我的平台'  # 平台中文名

    def fetch_blogger_info(self, blogger_id: str) -> Dict:
        # 获取博主信息
        return {
            'blogger_id': blogger_id,
            'username': '...',
            'nickname': '...',
            # ... 其他字段
        }

    def fetch_posts(self, blogger_id: str, page: int = 1, **kwargs) -> List[Dict]:
        # 获取推文列表
        posts = []
        # ... 爬取逻辑
        return posts
```

### 步骤 2: 注册爬虫

```python
from crawler.crawler_manager import CrawlerFactory
from myapp.crawlers import MyPlatformCrawler

# 注册新平台
CrawlerFactory.register_crawler('my_platform', MyPlatformCrawler)
```

### 步骤 3: 使用新平台

```python
manager = get_crawler_manager()
result = manager.crawl_blogger('my_platform', 'blogger_id_123')
```

## 配置

编辑 `crawler/config.py` 配置各平台参数:

```python
PLATFORM_CONFIG = {
    'weibo': {
        'use_api': False,
        'access_token': os.getenv('WEIBO_ACCESS_TOKEN', ''),
        'delay': 2.0,
        'max_pages': 10,
    },
    # ... 其他平台
}
```

## 环境变量

创建 `.env` 文件设置敏感信息:

```bash
# 微博
WEIBO_ACCESS_TOKEN=your_token_here
WEIBO_COOKIE=your_cookie_here

# Social Truth
SOCIAL_TRUTH_API_KEY=your_api_key_here

# Twitter
TWITTER_BEARER_TOKEN=your_token_here
```

## Django Admin

访问 `/admin/` 管理数据:

- **Blogger**: 查看和管理博主信息
- **Post**: 查看和搜索推文
- **CrawlerLog**: 查看爬虫历史日志

## 注意事项

### 反爬虫机制

1. **请求延迟**: 建议至少 2 秒延迟
2. **User-Agent**: 使用真实浏览器 UA
3. **Cookie**: 可能需要登录后的 Cookie
4. **IP 限制**: 注意 IP 访问频率

### API 使用

推荐使用官方 API:
- 微博开放平台: https://open.weibo.com/
- Twitter API: https://developer.twitter.com/

### 法律合规

- 遵守平台服务条款
- 不爬取私人数据
- 数据仅用于学习研究
- 注明数据来源

## 数据去重机制

### 1. 基于 post_id 去重
```python
# 数据库唯一约束
unique_together = [['platform', 'post_id']]
```

### 2. 基于 content_hash 去重
```python
# 生成内容哈希
content_to_hash = f"{platform}_{post_id}_{content}"
content_hash = hashlib.md5(content_to_hash.encode()).hexdigest()
```

## 增量爬取

```python
# 第一次爬取
crawler.crawl_blogger('bobo123')

# 后续自动增量爬取(从上次最后推文开始)
crawler.crawl_blogger('bobo123')
```

## 下一步开发

- [ ] 定时任务调度
- [ ] 代理 IP 支持
- [ ] 分布式爬取
- [ ] 数据分析和可视化
- [ ] 更多平台支持(Twitter, Facebook等)
- [ ] 异步爬取支持
- [ ] 失败重试机制

## 许可证

MIT License
