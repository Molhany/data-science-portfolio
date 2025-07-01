from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PageView, PortfolioMetrics, ContentInteraction, 
    SkillAnalytics, ProjectAnalytics
)


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = [
        'page_url', 'page_title', 'ip_address', 'country', 
        'device_type', 'browser', 'time_on_page', 'created_at'
    ]
    list_filter = [
        'device_type', 'country', 'browser', 'is_unique_visitor', 'created_at'
    ]
    search_fields = ['page_url', 'page_title', 'ip_address', 'referrer']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Page Information', {
            'fields': ('page_url', 'page_title', 'time_on_page')
        }),
        ('Visitor Information', {
            'fields': ('ip_address', 'session_id', 'is_unique_visitor')
        }),
        ('Geographic Data', {
            'fields': ('country', 'city')
        }),
        ('Device Information', {
            'fields': ('device_type', 'browser', 'operating_system', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Referrer', {
            'fields': ('referrer',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PortfolioMetrics)
class PortfolioMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'date', 'total_page_views', 'unique_visitors', 'bounce_rate',
        'contact_form_submissions', 'project_views', 'blog_post_views'
    ]
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Traffic Metrics', {
            'fields': (
                'total_page_views', 'unique_visitors', 'bounce_rate', 
                'avg_session_duration'
            )
        }),
        ('Content Metrics', {
            'fields': (
                'most_viewed_page', 'most_viewed_project', 'most_viewed_blog_post'
            )
        }),
        ('Engagement Metrics', {
            'fields': (
                'contact_form_submissions', 'newsletter_signups', 
                'project_views', 'blog_post_views'
            )
        }),
        ('Geographic Data', {
            'fields': ('top_countries', 'top_cities'),
            'classes': ('collapse',)
        }),
        ('Device Data', {
            'fields': ('desktop_percentage', 'mobile_percentage', 'tablet_percentage'),
            'classes': ('collapse',)
        }),
        ('Referrer Data', {
            'fields': ('top_referrers',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContentInteraction)
class ContentInteractionAdmin(admin.ModelAdmin):
    list_display = [
        'content_object', 'interaction_type', 'ip_address', 'created_at'
    ]
    list_filter = ['interaction_type', 'content_type', 'created_at']
    search_fields = ['ip_address']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(SkillAnalytics)
class SkillAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'skill_name', 'page_views', 'project_associations', 
        'blog_mentions', 'job_market_demand', 'last_updated'
    ]
    list_filter = ['job_market_demand', 'last_updated']
    search_fields = ['skill_name']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('Skill Information', {
            'fields': ('skill_name',)
        }),
        ('Interest Metrics', {
            'fields': ('page_views', 'project_associations', 'blog_mentions')
        }),
        ('Progression Data', {
            'fields': ('proficiency_changes', 'certification_dates'),
            'classes': ('collapse',)
        }),
        ('Market Data', {
            'fields': ('job_market_demand',)
        }),
        ('Timestamp', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProjectAnalytics)
class ProjectAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'project_title', 'total_views', 'unique_views', 
        'github_clicks', 'demo_clicks', 'shares', 'last_updated'
    ]
    list_filter = ['last_updated']
    search_fields = ['project_title', 'project_slug']
    readonly_fields = ['last_updated']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('project_slug', 'project_title')
        }),
        ('View Metrics', {
            'fields': ('total_views', 'unique_views', 'avg_time_on_page')
        }),
        ('Engagement Metrics', {
            'fields': ('github_clicks', 'demo_clicks', 'documentation_clicks')
        }),
        ('Social Metrics', {
            'fields': ('shares', 'likes')
        }),
        ('Conversion Metrics', {
            'fields': ('contact_inquiries',)
        }),
        ('Timestamp', {
            'fields': ('last_updated',),
            'classes': ('collapse',)
        }),
    )
