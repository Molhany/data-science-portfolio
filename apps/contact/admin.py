from django.contrib import admin
from django.utils.html import format_html
from .models import ContactMessage, NewsletterSubscription, ContactFormSubmission


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'subject', 'message_type', 'status', 
        'priority', 'created_at', 'read_at'
    ]
    list_filter = [
        'status', 'priority', 'message_type', 'created_at', 'read_at'
    ]
    search_fields = ['name', 'email', 'subject', 'message', 'company']
    readonly_fields = ['created_at', 'read_at', 'replied_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'company', 'website')
        }),
        ('Message Details', {
            'fields': ('subject', 'message', 'message_type')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'user_agent', 'referrer'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'read_at', 'replied_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_replied', 'set_high_priority']
    
    def mark_as_read(self, request, queryset):
        for message in queryset:
            message.mark_as_read()
        self.message_user(request, f'{queryset.count()} messages marked as read.')
    mark_as_read.short_description = 'Mark selected messages as read'
    
    def mark_as_replied(self, request, queryset):
        for message in queryset:
            message.mark_as_replied()
        self.message_user(request, f'{queryset.count()} messages marked as replied.')
    mark_as_replied.short_description = 'Mark selected messages as replied'
    
    def set_high_priority(self, request, queryset):
        queryset.update(priority='high')
        self.message_user(request, f'{queryset.count()} messages set to high priority.')
    set_high_priority.short_description = 'Set selected messages to high priority'


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'name', 'is_active', 'is_verified', 
        'interests_preview', 'subscribed_at'
    ]
    list_filter = ['is_active', 'is_verified', 'subscribed_at']
    search_fields = ['email', 'name', 'interests']
    readonly_fields = ['subscribed_at', 'unsubscribed_at', 'verification_token']
    date_hierarchy = 'subscribed_at'
    
    fieldsets = (
        ('Subscription Details', {
            'fields': ('email', 'name', 'is_active', 'is_verified')
        }),
        ('Preferences', {
            'fields': ('interests',)
        }),
        ('Metadata', {
            'fields': ('ip_address', 'source'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('verification_token',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('subscribed_at', 'unsubscribed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def interests_preview(self, obj):
        interests = obj.get_interests_list()
        if interests:
            return ', '.join(interests[:3]) + ('...' if len(interests) > 3 else '')
        return 'None'
    interests_preview.short_description = 'Interests'
    
    actions = ['activate_subscriptions', 'deactivate_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f'{queryset.count()} subscriptions activated.')
    activate_subscriptions.short_description = 'Activate selected subscriptions'
    
    def deactivate_subscriptions(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f'{queryset.count()} subscriptions deactivated.')
    deactivate_subscriptions.short_description = 'Deactivate selected subscriptions'


@admin.register(ContactFormSubmission)
class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        'form_name', 'page_url', 'is_successful', 'created_at'
    ]
    list_filter = ['form_name', 'is_successful', 'created_at']
    search_fields = ['form_name', 'page_url', 'error_message']
    readonly_fields = ['created_at', 'submission_data']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Form Details', {
            'fields': ('form_name', 'page_url', 'is_successful')
        }),
        ('Submission Data', {
            'fields': ('submission_data',),
            'classes': ('collapse',)
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('ip_address', 'user_agent', 'referrer', 'session_id'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
