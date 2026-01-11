from django.db import models
from django.contrib.auth import get_user_model
import hashlib
import json


class SocialMediaPlatform(models.TextChoices):
    """社交媒体平台枚举"""
    WEIBO = 'weibo', '微博'
    SOCIAL_TRUTH = 'social_truth', 'Social Truth'
    TWITTER = 'twitter', 'Twitter'
    FACEBOOK = 'facebook', 'Facebook'


class Blogger(models.Model):
    """博主信息模型"""
    platform = models.CharField(
        max_length=20,
        choices=SocialMediaPlatform.choices,
        verbose_name='平台'
    )
    blogger_id = models.CharField(max_length=100, verbose_name='博主ID')
    username = models.CharField(max_length=100, verbose_name='用户名')
    nickname = models.CharField(max_length=200, blank=True, verbose_name='昵称')
    avatar_url = models.URLField(blank=True, verbose_name='头像URL')
    homepage_url = models.URLField(blank=True, verbose_name='主页URL')
    description = models.TextField(blank=True, verbose_name='简介')
    followers_count = models.IntegerField(default=0, verbose_name='粉丝数')
    following_count = models.IntegerField(default=0, verbose_name='关注数')
    posts_count = models.IntegerField(default=0, verbose_name='微博数')

    # 爬取相关
    is_active = models.BooleanField(default=True, verbose_name='是否活跃')
    last_crawled_at = models.DateTimeField(null=True, blank=True, verbose_name='最后爬取时间')
    last_post_id = models.CharField(max_length=100, blank=True, verbose_name='最后爬取的推文ID')
    last_post_time = models.DateTimeField(null=True, blank=True, verbose_name='最后爬取的推文时间')

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '博主'
        verbose_name_plural = '博主'
        unique_together = [['platform', 'blogger_id']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['platform', 'blogger_id']),
            models.Index(fields=['is_active']),
            models.Index(fields=['last_crawled_at']),
        ]

    def __str__(self):
        return f"{self.get_platform_display()} - {self.nickname or self.username}"


class Post(models.Model):
    """推文/帖子模型"""
    # 关联博主
    blogger = models.ForeignKey(
        Blogger,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='博主'
    )

    # 基本信息
    platform = models.CharField(
        max_length=20,
        choices=SocialMediaPlatform.choices,
        verbose_name='平台'
    )
    post_id = models.CharField(max_length=100, verbose_name='推文ID')
    content = models.TextField(verbose_name='内容')
    raw_content = models.TextField(blank=True, verbose_name='原始内容(JSON)')

    # 媒体内容 (使用TextField存储JSON以兼容SQLite)
    images = models.TextField(default='[]', blank=True, verbose_name='图片URL列表(JSON)')
    videos = models.TextField(default='[]', blank=True, verbose_name='视频URL列表(JSON)')
    external_links = models.TextField(default='[]', blank=True, verbose_name='外部链接(JSON)')

    # 互动数据
    likes_count = models.IntegerField(default=0, verbose_name='点赞数')
    comments_count = models.IntegerField(default=0, verbose_name='评论数')
    reposts_count = models.IntegerField(default=0, verbose_name='转发数')

    # 时间信息
    published_at = models.DateTimeField(verbose_name='发布时间')
    crawled_at = models.DateTimeField(auto_now_add=True, verbose_name='爬取时间')

    # 关联信息
    is_repost = models.BooleanField(default=False, verbose_name='是否转发')
    original_post_id = models.CharField(max_length=100, blank=True, verbose_name='原推文ID')
    original_post_url = models.URLField(blank=True, verbose_name='原推文链接')

    # 去重用
    content_hash = models.CharField(max_length=32, verbose_name='内容哈希', db_index=True)

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '推文'
        verbose_name_plural = '推文'
        unique_together = [['platform', 'post_id']]
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['platform', 'post_id']),
            models.Index(fields=['content_hash']),
            models.Index(fields=['blogger', 'published_at']),
            models.Index(fields=['-published_at']),
        ]

    def __str__(self):
        content_preview = self.content[:50] if self.content else ''
        return f"{self.blogger.nickname}: {content_preview}..."

    @property
    def images_list(self):
        """获取图片列表"""
        try:
            return json.loads(self.images) if self.images else []
        except:
            return []

    @property
    def videos_list(self):
        """获取视频列表"""
        try:
            return json.loads(self.videos) if self.videos else []
        except:
            return []

    @property
    def external_links_list(self):
        """获取外部链接列表"""
        try:
            return json.loads(self.external_links) if self.external_links else []
        except:
            return []

    def set_images(self, images_list):
        """设置图片列表"""
        self.images = json.dumps(images_list, ensure_ascii=False)

    def set_videos(self, videos_list):
        """设置视频列表"""
        self.videos = json.dumps(videos_list, ensure_ascii=False)

    def set_external_links(self, links_list):
        """设置外部链接列表"""
        self.external_links = json.dumps(links_list, ensure_ascii=False)

    def save(self, *args, **kwargs):
        """保存时生成内容哈希用于去重"""
        if not self.content_hash:
            # 使用内容的MD5作为哈希值
            content_to_hash = f"{self.platform}_{self.post_id}_{self.content}"
            self.content_hash = hashlib.md5(content_to_hash.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)


class CrawlerLog(models.Model):
    """爬虫日志模型"""
    platform = models.CharField(
        max_length=20,
        choices=SocialMediaPlatform.choices,
        verbose_name='平台'
    )
    blogger = models.ForeignKey(
        Blogger,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='crawler_logs',
        verbose_name='博主'
    )

    # 爬取结果
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', '成功'),
            ('failed', '失败'),
            ('partial', '部分成功'),
        ],
        verbose_name='状态'
    )
    posts_found = models.IntegerField(default=0, verbose_name='发现推文数')
    posts_new = models.IntegerField(default=0, verbose_name='新增推文数')
    posts_duplicate = models.IntegerField(default=0, verbose_name='重复推文数')

    # 错误信息
    error_message = models.TextField(blank=True, verbose_name='错误信息')

    # 时间信息
    started_at = models.DateTimeField(verbose_name='开始时间')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    duration_seconds = models.IntegerField(null=True, blank=True, verbose_name='耗时(秒)')

    # 元数据
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '爬虫日志'
        verbose_name_plural = '爬虫日志'
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['platform']),
            models.Index(fields=['status']),
            models.Index(fields=['-started_at']),
        ]

    def __str__(self):
        return f"{self.get_platform_display()} - {self.get_status_display()} - {self.started_at}"
