"""
爬虫管理器
统一管理所有爬虫实例
"""
from typing import Dict, Type
from crawler.base_crawler import BaseCrawler
from crawler.weibo_crawler import WeiboCrawler, WeiboAPICrawler
from crawler.social_truth_crawler import SocialTruthCrawler, SocialTruthAPICrawler


class CrawlerFactory:
    """
    爬虫工厂类
    根据平台类型创建对应的爬虫实例
    """

    # 注册的爬虫类
    _crawler_classes: Dict[str, Type[BaseCrawler]] = {
        'weibo': WeiboCrawler,
        'social_truth': SocialTruthCrawler,
    }

    @classmethod
    def register_crawler(cls, platform: str, crawler_class: Type[BaseCrawler]):
        """
        注册新的爬虫类

        Args:
            platform: 平台标识
            crawler_class: 爬虫类
        """
        cls._crawler_classes[platform] = crawler_class

    @classmethod
    def create_crawler(cls, platform: str, **kwargs) -> BaseCrawler:
        """
        创建爬虫实例

        Args:
            platform: 平台标识 (weibo, social_truth等)
            **kwargs: 传递给爬虫构造函数的参数

        Returns:
            爬虫实例

        Raises:
            ValueError: 不支持的平台
        """
        crawler_class = cls._crawler_classes.get(platform)

        if not crawler_class:
            raise ValueError(
                f"Unsupported platform: {platform}. "
                f"Supported platforms: {list(cls._crawler_classes.keys())}"
            )

        return crawler_class(**kwargs)

    @classmethod
    def get_supported_platforms(cls) -> list:
        """
        获取支持的平台列表

        Returns:
            平台标识列表
        """
        return list(cls._crawler_classes.keys())


class CrawlerManager:
    """
    爬虫管理器

    提供统一的爬虫管理接口
    """

    def __init__(self):
        """初始化管理器"""
        self._crawlers: Dict[str, BaseCrawler] = {}

    def get_or_create_crawler(
        self,
        platform: str,
        force_new: bool = False,
        **kwargs
    ) -> BaseCrawler:
        """
        获取或创建爬虫实例

        Args:
            platform: 平台标识
            force_new: 是否强制创建新实例
            **kwargs: 传递给爬虫构造函数的参数

        Returns:
            爬虫实例
        """
        if force_new or platform not in self._crawlers:
            crawler = CrawlerFactory.create_crawler(platform, **kwargs)
            self._crawlers[platform] = crawler

        return self._crawlers[platform]

    def crawl_blogger(
        self,
        platform: str,
        blogger_id: str,
        **kwargs
    ) -> dict:
        """
        爬取博主推文

        Args:
            platform: 平台标识
            blogger_id: 博主ID
            **kwargs: 传递给爬虫方法的参数

        Returns:
            爬取结果
        """
        crawler = self.get_or_create_crawler(platform)
        return crawler.crawl_blogger(blogger_id, **kwargs)

    def crawl_multiple_bloggers(
        self,
        platform: str,
        blogger_ids: list,
        **kwargs
    ) -> list:
        """
        批量爬取多个博主

        Args:
            platform: 平台标识
            blogger_ids: 博主ID列表
            **kwargs: 传递给爬虫方法的参数

        Returns:
            爬取结果列表
        """
        crawler = self.get_or_create_crawler(platform)
        return crawler.crawl_multiple_bloggers(blogger_ids, **kwargs)

    def get_supported_platforms(self) -> list:
        """
        获取支持的平台列表

        Returns:
            平台标识列表
        """
        return CrawlerFactory.get_supported_platforms()


# 全局单例
_manager_instance = None


def get_crawler_manager() -> CrawlerManager:
    """
    获取爬虫管理器单例

    Returns:
        CrawlerManager实例
    """
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = CrawlerManager()
    return _manager_instance
