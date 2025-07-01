from django.contrib import admin
from django.utils.html import format_html
from .models import ProjectCategory, Technology, Project, ProjectImage, ProjectLink


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'projects_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects'


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'projects_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def projects_count(self, obj):
        return obj.projects.count()
    projects_count.short_description = 'Projects'


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'display_order']


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1
    fields = ['title', 'url', 'link_type', 'description']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'has_video', 'has_image', 'is_featured',
        'is_published', 'start_date', 'technologies_list', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'is_published', 'category', 
        'technologies', 'start_date', 'created_at'
    ]
    search_fields = ['title', 'description', 'short_description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'image_preview', 'video_preview']
    filter_horizontal = ['technologies']
    inlines = [ProjectImageInline, ProjectLinkInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description', 'category')
        }),
        ('Media', {
            'fields': ('featured_image', 'image_preview', 'demo_video', 'video_preview'),
            'description': 'Upload project media files. Video files should be in MP4 format for best compatibility.'
        }),
        ('Project Details', {
            'fields': (
                'technologies', 'status', 'start_date', 'end_date', 
                'duration_hours', 'key_features'
            )
        }),
        ('Links', {
            'fields': ('github_url', 'live_demo_url', 'documentation_url')
        }),
        ('Project Insights', {
            'fields': ('challenges_faced', 'lessons_learned'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_published', 'display_order')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def technologies_list(self, obj):
        return ', '.join([tech.name for tech in obj.technologies.all()[:3]])
    technologies_list.short_description = 'Technologies'

    def has_video(self, obj):
        if obj.demo_video:
            return format_html(
                '<span style="color: green;">✓ Video</span>'
            )
        return format_html('<span style="color: red;">✗ No Video</span>')
    has_video.short_description = 'Demo Video'
    has_video.admin_order_field = 'demo_video'

    def has_image(self, obj):
        if obj.featured_image:
            return format_html(
                '<span style="color: green;">✓ Image</span>'
            )
        return format_html('<span style="color: red;">✗ No Image</span>')
    has_image.short_description = 'Featured Image'
    has_image.admin_order_field = 'featured_image'

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.featured_image.url
            )
        return format_html('<p style="color: #666; font-style: italic;">No image uploaded</p>')
    image_preview.short_description = 'Image Preview'

    def video_preview(self, obj):
        if obj.demo_video:
            return format_html(
                '''
                <div style="max-width: 300px;">
                    <video controls style="width: 100%; max-height: 150px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <source src="{}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <p style="margin-top: 8px; font-size: 12px; color: #666;">
                        <strong>File:</strong> {}<br>
                        <strong>Size:</strong> {:.2f} MB
                    </p>
                </div>
                ''',
                obj.demo_video.url,
                obj.demo_video.name.split('/')[-1],
                obj.demo_video.size / (1024 * 1024) if obj.demo_video.size else 0
            )
        return format_html(
            '''
            <div style="padding: 20px; text-align: center; border: 2px dashed #ddd; border-radius: 8px; background-color: #f9f9f9;">
                <p style="color: #666; font-style: italic; margin: 0;">No demo video uploaded</p>
                <p style="color: #999; font-size: 12px; margin: 5px 0 0 0;">Supported formats: MP4, WebM, OGG</p>
            </div>
            '''
        )
    video_preview.short_description = 'Video Preview'
    
    actions = ['mark_as_featured', 'mark_as_published', 'mark_as_draft']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} projects marked as featured.')
    mark_as_featured.short_description = 'Mark selected projects as featured'
    
    def mark_as_published(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f'{queryset.count()} projects published.')
    mark_as_published.short_description = 'Publish selected projects'
    
    def mark_as_draft(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f'{queryset.count()} projects marked as draft.')
    mark_as_draft.short_description = 'Mark selected projects as draft'


@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'display_order', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['project__title', 'caption']
    ordering = ['project', 'display_order']


@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = ['project', 'title', 'link_type', 'url', 'created_at']
    list_filter = ['link_type', 'created_at']
    search_fields = ['project__title', 'title', 'description']
    ordering = ['project', 'link_type']
