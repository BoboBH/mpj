"""
爬虫配置文件
"""
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 爬虫通用配置
CRAWLER_CONFIG = {
    # 默认最大爬取页数
    'max_pages': 10,

    # 默认请求延迟(秒)
    'default_delay': 2.0,

    # 请求超时时间(秒)
    'request_timeout': 30,

    # 是否启用日志
    'enable_logging': True,

    # 日志级别
    'log_level': 'INFO',

    # 是否保存原始数据
    'save_raw_data': True,
}

# 各平台特定配置
PLATFORM_CONFIG = {
    'weibo': {
        # 是否使用API
        'use_api': False,

        # API访问令牌 (如果使用API)
        'access_token': os.getenv('WEIBO_ACCESS_TOKEN', ''),

        # 基础URL
        'base_url': 'https://weibo.com/ajax',

        # 请求延迟
        'delay': 2.0,

        # 最大页数
        'max_pages': 10,

        # Cookie (如果使用爬虫方式)
        'cookie': os.getenv('WEIBO_COOKIE', ''),
    },

    'social_truth': {
        # API密钥
        'api_key': os.getenv('SOCIAL_TRUTH_API_KEY', ''),

        # 基础URL
        'base_url': 'https://api.socialtruth.com/v1',

        # 请求延迟
        'delay': 2.0,

        # 最大页数
        'max_pages': 10,
    },

    'twitter': {
        'api_key': os.getenv('TWITTER_API_KEY', ''),
        'api_secret': os.getenv('TWITTER_API_SECRET', ''),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN', ''),
        'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET', ''),
        'bearer_token': os.getenv('TWITTER_BEARER_TOKEN', ''),
        'delay': 1.0,
        'max_pages': 10,
    },

    'facebook': {
        'app_id': os.getenv('FACEBOOK_APP_ID', ''),
        'app_secret': os.getenv('FACEBOOK_APP_SECRET', ''),
        'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN', ''),
        'delay': 2.0,
        'max_pages': 10,
    },
}

# 去重配置
DEDUPLICATION_CONFIG = {
    # 是否启用去重
    'enabled': True,

    # 去重方法: 'hash' (内容哈希) 或 'id' (推文ID)
    'method': 'both',

    # 是否检测相似内容
    'detect_similar': False,

    # 相似度阈值 (0-1)
    'similarity_threshold': 0.85,
}

# 数据库配置
DATABASE_CONFIG = {
    # 批量插入大小
    'batch_size': 100,

    # 是否使用bulk_create
    'use_bulk_create': True,
}

# 调度配置
SCHEDULER_CONFIG = {
    # 是否启用定时任务
    'enabled': False,

    # 爬取间隔 (分钟)
    'interval_minutes': 60,

    # 每次爬取的博主数量
    'batch_size': 10,
}


def get_config(platform: str = None) -> dict:
    """
    获取配置

    Args:
        platform: 平台标识,如果为None则返回通用配置

    Returns:
        配置字典
    """
    if platform:
        return {
            **CRAWLER_CONFIG,
            **PLATFORM_CONFIG.get(platform, {})
        }
    return CRAWLER_CONFIG


def get_platform_config(platform: str) -> dict:
    """
    获取平台特定配置

    Args:
        platform: 平台标识

    Returns:
        平台配置字典
    """
    return PLATFORM_CONFIG.get(platform, {})
