from django.contrib import admin
from .models import Blogger, Post, CrawlerLog


@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    """博主管理界面"""
    list_display = [
        'platform',
        'username',
        'nickname',
        'followers_count',
        'posts_count',
        'is_active',
        'last_crawled_at',
        'created_at',
    ]
    list_filter = ['platform', 'is_active', 'created_at']
    search_fields = ['username', 'nickname', 'blogger_id']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('platform', 'blogger_id', 'username', 'nickname', 'avatar_url', 'homepage_url')
        }),
        ('统计信息', {
            'fields': ('followers_count', 'following_count', 'posts_count')
        }),
        ('简介', {
            'fields': ('description',)
        }),
        ('爬取设置', {
            'fields': ('is_active', 'last_crawled_at', 'last_post_id', 'last_post_time')
        }),
        ('元数据', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'created_at'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """推文管理界面"""
    list_display = [
        'platform',
        'blogger',
        'content_preview',
        'published_at',
        'likes_count',
        'comments_count',
        'reposts_count',
        'is_repost',
        'crawled_at',
    ]
    list_filter = ['platform', 'is_repost', 'published_at', 'crawled_at']
    search_fields = ['content', 'post_id', 'blogger__username', 'blogger__nickname']
    readonly_fields = ['content_hash', 'crawled_at', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('blogger', 'platform', 'post_id', 'content')
        }),
        ('媒体内容', {
            'fields': ('images', 'videos', 'external_links'),
            'classes': ('collapse',)
        }),
        ('互动数据', {
            'fields': ('likes_count', 'comments_count', 'reposts_count')
        }),
        ('时间信息', {
            'fields': ('published_at', 'crawled_at')
        }),
        ('转发信息', {
            'fields': ('is_repost', 'original_post_id', 'original_post_url'),
            'classes': ('collapse',)
        }),
        ('原始数据', {
            'fields': ('raw_content',),
            'classes': ('collapse',)
        }),
        ('元数据', {
            'fields': ('content_hash', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'published_at'

    def content_preview(self, obj):
        """内容预览"""
        max_length = 50
        if len(obj.content) > max_length:
            return obj.content[:max_length] + '...'
        return obj.content
    content_preview.short_description = '内容'


@admin.register(CrawlerLog)
class CrawlerLogAdmin(admin.ModelAdmin):
    """爬虫日志管理界面"""
    list_display = [
        'platform',
        'blogger',
        'status',
        'posts_found',
        'posts_new',
        'posts_duplicate',
        'duration_seconds',
        'started_at',
    ]
    list_filter = ['platform', 'status', 'started_at']
    search_fields = ['blogger__username', 'blogger__nickname', 'error_message']
    readonly_fields = ['created_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('platform', 'blogger', 'status')
        }),
        ('爬取结果', {
            'fields': ('posts_found', 'posts_new', 'posts_duplicate')
        }),
        ('时间信息', {
            'fields': ('started_at', 'finished_at', 'duration_seconds')
        }),
        ('错误信息', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('元数据', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    date_hierarchy = 'started_at'

    def has_add_permission(self, request):
        """禁止手动添加日志"""
        return False

    def has_change_permission(self, request, obj=None):
        """日志只读"""
        return False
