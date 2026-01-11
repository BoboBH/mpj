"""
爬虫基类模块
提供所有爬虫的通用接口和功能
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Generator
from datetime import datetime
from django.utils import timezone
import logging
import time
import json

from crawler.models import Blogger, Post, CrawlerLog, SocialMediaPlatform


logger = logging.getLogger(__name__)


class BaseCrawler(ABC):
    """
    社交媒体爬虫基类

    功能:
    1. 支持翻页爬取博主推文
    2. 自动去重(基于post_id和content_hash)
    3. 记录最后爬取时间,避免重复爬取
    4. 记录爬取日志
    """

    # 子类需要定义的类属性
    platform: str = None  # 平台名称,如 'weibo'
    platform_name: str = None  # 平台中文名,如 '微博'

    def __init__(self, max_pages: int = 10, delay: float = 1.0):
        """
        初始化爬虫

        Args:
            max_pages: 最多爬取的页数
            delay: 每次请求之间的延迟(秒)
        """
        self.max_pages = max_pages
        self.delay = delay
        self.log_data = {
            'posts_found': 0,
            'posts_new': 0,
            'posts_duplicate': 0,
        }

    @abstractmethod
    def fetch_blogger_info(self, blogger_id: str) -> Dict:
        """
        获取博主信息

        Args:
            blogger_id: 博主ID

        Returns:
            包含博主信息的字典,格式如下:
            {
                'blogger_id': str,
                'username': str,
                'nickname': str,
                'avatar_url': str,
                'homepage_url': str,
                'description': str,
                'followers_count': int,
                'following_count': int,
                'posts_count': int,
            }
        """
        pass

    @abstractmethod
    def fetch_posts(self, blogger_id: str, page: int = 1, **kwargs) -> List[Dict]:
        """
        获取博主的推文列表

        Args:
            blogger_id: 博主ID
            page: 页码
            **kwargs: 其他参数(如since_id用于增量爬取)

        Returns:
            推文列表,每个推文包含:
            {
                'post_id': str,
                'content': str,
                'published_at': datetime,
                'likes_count': int,
                'comments_count': int,
                'reposts_count': int,
                'images': List[str],
                'videos': List[str],
                'external_links': List[str],
                'is_repost': bool,
                'original_post_id': str,
                'original_post_url': str,
                'raw_content': str,  # 原始JSON数据
            }
        """
        pass

    def get_or_create_blogger(self, blogger_id: str) -> Blogger:
        """
        获取或创建博主对象

        Args:
            blogger_id: 博主ID

        Returns:
            Blogger对象
        """
        blogger, created = Blogger.objects.get_or_create(
            platform=self.platform,
            blogger_id=blogger_id,
            defaults={
                'username': blogger_id,
            }
        )

        if created:
            logger.info(f"Created new blogger: {self.platform_name} - {blogger_id}")

        return blogger

    def update_blogger_info(self, blogger: Blogger, blogger_info: Dict):
        """
        更新博主信息

        Args:
            blogger: Blogger对象
            blogger_info: 博主信息字典
        """
        blogger.username = blogger_info.get('username', blogger.username)
        blogger.nickname = blogger_info.get('nickname', '')
        blogger.avatar_url = blogger_info.get('avatar_url', '')
        blogger.homepage_url = blogger_info.get('homepage_url', '')
        blogger.description = blogger_info.get('description', '')
        blogger.followers_count = blogger_info.get('followers_count', 0)
        blogger.following_count = blogger_info.get('following_count', 0)
        blogger.posts_count = blogger_info.get('posts_count', 0)
        blogger.save()

        logger.info(f"Updated blogger info: {blogger}")

    def save_post(self, blogger: Blogger, post_data: Dict) -> Optional[Post]:
        """
        保存推文,自动去重

        Args:
            blogger: Blogger对象
            post_data: 推文数据字典

        Returns:
            Post对象,如果推文已存在则返回None
        """
        post_id = post_data['post_id']

        # 检查是否已存在(基于platform和post_id)
        if Post.objects.filter(platform=self.platform, post_id=post_id).exists():
            logger.debug(f"Post already exists: {post_id}")
            self.log_data['posts_duplicate'] += 1
            return None

        # 创建新推文
        post = Post(
            blogger=blogger,
            platform=self.platform,
            post_id=post_id,
            content=post_data.get('content', ''),
            raw_content=post_data.get('raw_content', ''),
            likes_count=post_data.get('likes_count', 0),
            comments_count=post_data.get('comments_count', 0),
            reposts_count=post_data.get('reposts_count', 0),
            published_at=post_data['published_at'],
            is_repost=post_data.get('is_repost', False),
            original_post_id=post_data.get('original_post_id', ''),
            original_post_url=post_data.get('original_post_url', ''),
        )

        # 使用setter方法设置JSON字段
        post.set_images(post_data.get('images', []))
        post.set_videos(post_data.get('videos', []))
        post.set_external_links(post_data.get('external_links', []))

        post.save()

        logger.info(f"Saved new post: {post_id}")
        self.log_data['posts_new'] += 1
        return post

    def crawl_blogger(
        self,
        blogger_id: str,
        max_pages: Optional[int] = None,
        since_id: Optional[str] = None,
        update_blogger_info: bool = True,
    ) -> Dict:
        """
        爬取博主的所有推文

        Args:
            blogger_id: 博主ID
            max_pages: 最多爬取页数,默认使用self.max_pages
            since_id: 从此推文ID之后开始爬取(增量爬取)
            update_blogger_info: 是否更新博主信息

        Returns:
            爬取结果统计:
            {
                'success': bool,
                'posts_found': int,
                'posts_new': int,
                'posts_duplicate': int,
                'last_post_id': str,
                'last_post_time': datetime,
                'error_message': str,
            }
        """
        start_time = timezone.now()
        self.log_data = {
            'posts_found': 0,
            'posts_new': 0,
            'posts_duplicate': 0,
        }

        # 创建日志记录
        log = CrawlerLog.objects.create(
            platform=self.platform,
            started_at=start_time,
        )

        max_pages = max_pages or self.max_pages
        error_message = ''

        try:
            # 获取或创建博主
            blogger = self.get_or_create_blogger(blogger_id)
            log.blogger = blogger
            log.save()

            # 更新博主信息
            if update_blogger_info:
                try:
                    blogger_info = self.fetch_blogger_info(blogger_id)
                    self.update_blogger_info(blogger, blogger_info)
                except Exception as e:
                    logger.warning(f"Failed to fetch blogger info: {e}")
                    error_message += f"Failed to fetch blogger info: {str(e)}; "

            # 准备爬取参数
            crawl_kwargs = {}
            if since_id:
                crawl_kwargs['since_id'] = since_id
            elif blogger.last_post_id:
                crawl_kwargs['since_id'] = blogger.last_post_id

            last_post_id = ''
            last_post_time = None
            has_more = True
            page = 1

            # 翻页爬取
            while has_more and page <= max_pages:
                logger.info(f"Crawling page {page}/{max_pages} for blogger {blogger_id}")

                try:
                    posts = self.fetch_posts(blogger_id, page=page, **crawl_kwargs)

                    if not posts:
                        logger.info(f"No more posts found at page {page}")
                        has_more = False
                        break

                    self.log_data['posts_found'] += len(posts)

                    # 保存推文
                    for post_data in posts:
                        post = self.save_post(blogger, post_data)
                        if post:
                            last_post_id = post.post_id
                            last_post_time = post.published_at

                    # 延迟,避免请求过快
                    if page < max_pages:
                        time.sleep(self.delay)

                    page += 1

                except Exception as e:
                    logger.error(f"Error crawling page {page}: {e}")
                    error_message += f"Error at page {page}: {str(e)}; "
                    has_more = False
                    break

            # 更新博主的最后爬取信息
            blogger.last_crawled_at = timezone.now()
            if last_post_id:
                blogger.last_post_id = last_post_id
            if last_post_time:
                blogger.last_post_time = last_post_time
            blogger.save()

            logger.info(f"Crawl completed for blogger {blogger_id}: "
                       f"found={self.log_data['posts_found']}, "
                       f"new={self.log_data['posts_new']}, "
                       f"duplicate={self.log_data['posts_duplicate']}")

        except Exception as e:
            logger.exception(f"Fatal error crawling blogger {blogger_id}: {e}")
            error_message = f"Fatal error: {str(e)}"

        finally:
            # 更新日志
            end_time = timezone.now()
            log.status = 'success' if not error_message else ('partial' if self.log_data['posts_new'] > 0 else 'failed')
            log.posts_found = self.log_data['posts_found']
            log.posts_new = self.log_data['posts_new']
            log.posts_duplicate = self.log_data['posts_duplicate']
            log.error_message = error_message
            log.finished_at = end_time
            log.duration_seconds = int((end_time - start_time).total_seconds())
            log.save()

        return {
            'success': not error_message or self.log_data['posts_new'] > 0,
            'posts_found': self.log_data['posts_found'],
            'posts_new': self.log_data['posts_new'],
            'posts_duplicate': self.log_data['posts_duplicate'],
            'last_post_id': last_post_id,
            'last_post_time': last_post_time,
            'error_message': error_message,
        }

    def crawl_multiple_bloggers(
        self,
        blogger_ids: List[str],
        max_pages: Optional[int] = None,
    ) -> List[Dict]:
        """
        批量爬取多个博主

        Args:
            blogger_ids: 博主ID列表
            max_pages: 每个博主最多爬取页数

        Returns:
            每个博主的爬取结果列表
        """
        results = []

        for blogger_id in blogger_ids:
            logger.info(f"Starting crawl for blogger: {blogger_id}")
            result = self.crawl_blogger(blogger_id, max_pages=max_pages)
            results.append({
                'blogger_id': blogger_id,
                **result
            })

            # 博主之间的延迟
            time.sleep(self.delay)

        return results
