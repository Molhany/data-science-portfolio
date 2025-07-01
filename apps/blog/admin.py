from django.contrib import admin
from django.utils.html import format_html
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'posts_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Posts'


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'is_published', 'is_featured',
        'view_count', 'reading_time', 'published_at', 'created_at'
    ]
    list_filter = [
        'status', 'is_published', 'is_featured', 'category',
        'published_at', 'created_at'
    ]
    search_fields = ['title', 'content', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'view_count']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'category')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Metadata', {
            'fields': ('tags', 'reading_time')
        }),
        ('Publishing', {
            'fields': ('status', 'is_published', 'is_featured', 'published_at')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('view_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_published', 'mark_as_featured', 'mark_as_draft']
    
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True, status='published')
        self.message_user(request, f'{queryset.count()} posts published.')
    mark_as_published.short_description = 'Publish selected posts'
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} posts marked as featured.')
    mark_as_featured.short_description = 'Mark selected posts as featured'
    
    def mark_as_draft(self, request, queryset):
        queryset.update(is_published=False, status='draft')
        self.message_user(request, f'{queryset.count()} posts marked as draft.')
    mark_as_draft.short_description = 'Mark selected posts as draft'
