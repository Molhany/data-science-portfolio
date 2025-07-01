from django.contrib import admin
from django.utils.html import format_html
from .models import SkillCategory, Skill, SkillEndorsement, SkillProgress


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color_preview', 'skills_count', 'display_order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['display_order', 'name']
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%; display: inline-block;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color'
    
    def skills_count(self, obj):
        return obj.skills.count()
    skills_count.short_description = 'Skills'


class SkillEndorsementInline(admin.TabularInline):
    model = SkillEndorsement
    extra = 0
    fields = ['endorser_name', 'endorser_title', 'endorser_company', 'endorsement_text']


class SkillProgressInline(admin.TabularInline):
    model = SkillProgress
    extra = 0
    fields = ['proficiency_level', 'notes', 'milestone_achieved', 'recorded_at']
    readonly_fields = ['recorded_at']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'proficiency_level', 'proficiency_stars', 
        'years_of_experience', 'is_certified', 'is_featured', 'display_order'
    ]
    list_filter = [
        'category', 'proficiency_level', 'is_certified', 'is_featured', 
        'created_at'
    ]
    search_fields = ['name', 'description', 'certification_name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SkillEndorsementInline, SkillProgressInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'description')
        }),
        ('Proficiency', {
            'fields': ('proficiency_level', 'years_of_experience')
        }),
        ('Visual Elements', {
            'fields': ('icon', 'color')
        }),
        ('Certification', {
            'fields': (
                'is_certified', 'certification_name', 
                'certification_url', 'certification_date'
            ),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'display_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def proficiency_stars(self, obj):
        return obj.get_proficiency_stars()
    proficiency_stars.short_description = 'Stars'
    
    actions = ['mark_as_featured', 'mark_as_certified']
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} skills marked as featured.')
    mark_as_featured.short_description = 'Mark selected skills as featured'
    
    def mark_as_certified(self, request, queryset):
        queryset.update(is_certified=True)
        self.message_user(request, f'{queryset.count()} skills marked as certified.')
    mark_as_certified.short_description = 'Mark selected skills as certified'


@admin.register(SkillEndorsement)
class SkillEndorsementAdmin(admin.ModelAdmin):
    list_display = ['skill', 'endorser_name', 'endorser_title', 'endorser_company', 'created_at']
    list_filter = ['skill', 'created_at']
    search_fields = ['skill__name', 'endorser_name', 'endorser_company', 'endorsement_text']
    readonly_fields = ['created_at']


@admin.register(SkillProgress)
class SkillProgressAdmin(admin.ModelAdmin):
    list_display = ['skill', 'proficiency_level', 'milestone_achieved', 'recorded_at']
    list_filter = ['skill', 'proficiency_level', 'recorded_at']
    search_fields = ['skill__name', 'notes', 'milestone_achieved']
    readonly_fields = ['recorded_at']
    date_hierarchy = 'recorded_at'
