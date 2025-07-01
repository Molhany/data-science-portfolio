from django.contrib import admin
from .models import Profile, ProfileImage, Education, Experience, Achievement


class ProfileImageInline(admin.TabularInline):
    model = ProfileImage
    extra = 1
    fields = ['image', 'caption', 'is_active', 'display_order']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'title', 'email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProfileImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'bio', 'profile_image', 'resume')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Media Links', {
            'fields': (
                ('github_url', 'linkedin_url'),
                ('twitter_url', 'facebook_url'),
                ('instagram_url', 'youtube_url'),
                ('kaggle_url',)
            ),
            'description': 'Add your social media profile URLs'
        }),
        ('Contact Information', {
            'fields': (
                ('contact_email', 'contact_phone'),
                'contact_address',
                'business_hours'
            ),
            'description': 'Contact information displayed in footer and contact sections'
        }),
        ('Messaging Platforms', {
            'fields': (
                ('whatsapp_number', 'telegram_url'),
                ('discord_url', 'skype_username')
            ),
            'description': 'Messaging and communication platforms',
            'classes': ('collapse',)
        }),
        ('SEO & Meta', {
            'fields': ('meta_description', 'meta_keywords')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(ProfileImage)
class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ['profile', 'caption', 'is_active', 'display_order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['profile__name', 'caption']
    ordering = ['profile', 'display_order']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['institution', 'degree', 'field_of_study', 'start_date', 'end_date', 'is_current']
    list_filter = ['degree', 'is_current', 'start_date']
    search_fields = ['institution', 'field_of_study']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['company', 'position', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current', 'start_date']
    search_fields = ['company', 'position']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'date_received']
    list_filter = ['date_received', 'organization']
    search_fields = ['title', 'organization']
    date_hierarchy = 'date_received'
    readonly_fields = ['created_at', 'updated_at']
