from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class PageView(models.Model):
    """Track page views for analytics"""
    page_url = models.URLField()
    page_title = models.CharField(max_length=200, blank=True)
    
    # Visitor information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    referrer = models.URLField(blank=True)
    
    # Geographic data (can be populated via IP geolocation)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    # Session tracking
    session_id = models.CharField(max_length=100)
    is_unique_visitor = models.BooleanField(default=False)
    
    # Device information
    device_type = models.CharField(
        max_length=20,
        choices=[
            ('desktop', 'Desktop'),
            ('tablet', 'Tablet'),
            ('mobile', 'Mobile'),
            ('other', 'Other'),
        ],
        default='other'
    )
    browser = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    
    # Timing
    time_on_page = models.PositiveIntegerField(blank=True, null=True, help_text="Time in seconds")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Page View"
        verbose_name_plural = "Page Views"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.page_url} - {self.created_at.date()}"


class PortfolioMetrics(models.Model):
    """Daily aggregated metrics for the portfolio"""
    date = models.DateField(unique=True)
    
    # Traffic metrics
    total_page_views = models.PositiveIntegerField(default=0)
    unique_visitors = models.PositiveIntegerField(default=0)
    bounce_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    avg_session_duration = models.PositiveIntegerField(default=0, help_text="Average session duration in seconds")
    
    # Content metrics
    most_viewed_page = models.URLField(blank=True)
    most_viewed_project = models.CharField(max_length=200, blank=True)
    most_viewed_blog_post = models.CharField(max_length=200, blank=True)
    
    # Engagement metrics
    contact_form_submissions = models.PositiveIntegerField(default=0)
    newsletter_signups = models.PositiveIntegerField(default=0)
    project_views = models.PositiveIntegerField(default=0)
    blog_post_views = models.PositiveIntegerField(default=0)
    
    # Geographic data
    top_countries = models.JSONField(default=list, blank=True)
    top_cities = models.JSONField(default=list, blank=True)
    
    # Device data
    desktop_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    mobile_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    tablet_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    # Referrer data
    top_referrers = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Portfolio Metrics"
        verbose_name_plural = "Portfolio Metrics"
        ordering = ['-date']

    def __str__(self):
        return f"Metrics for {self.date}"


class ContentInteraction(models.Model):
    """Track interactions with specific content"""
    INTERACTION_TYPES = [
        ('view', 'View'),
        ('like', 'Like'),
        ('share', 'Share'),
        ('download', 'Download'),
        ('click', 'Click'),
        ('comment', 'Comment'),
    ]
    
    # Generic foreign key to any content
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    
    # User information
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    session_id = models.CharField(max_length=100)
    
    # Additional data
    interaction_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Content Interaction"
        verbose_name_plural = "Content Interactions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.interaction_type} on {self.content_object} - {self.created_at.date()}"


class SkillAnalytics(models.Model):
    """Analytics for skill progression and interest"""
    skill_name = models.CharField(max_length=100)
    
    # Interest metrics
    page_views = models.PositiveIntegerField(default=0)
    project_associations = models.PositiveIntegerField(default=0)
    blog_mentions = models.PositiveIntegerField(default=0)
    
    # Progression tracking
    proficiency_changes = models.JSONField(default=list, blank=True)
    certification_dates = models.JSONField(default=list, blank=True)
    
    # Market demand (can be updated manually or via APIs)
    job_market_demand = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('very_high', 'Very High'),
        ],
        default='medium'
    )
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill Analytics"
        verbose_name_plural = "Skill Analytics"
        ordering = ['-page_views']

    def __str__(self):
        return f"Analytics for {self.skill_name}"


class ProjectAnalytics(models.Model):
    """Analytics for individual projects"""
    project_slug = models.CharField(max_length=200, unique=True)
    project_title = models.CharField(max_length=200)
    
    # View metrics
    total_views = models.PositiveIntegerField(default=0)
    unique_views = models.PositiveIntegerField(default=0)
    avg_time_on_page = models.PositiveIntegerField(default=0, help_text="Average time in seconds")
    
    # Engagement metrics
    github_clicks = models.PositiveIntegerField(default=0)
    demo_clicks = models.PositiveIntegerField(default=0)
    documentation_clicks = models.PositiveIntegerField(default=0)
    
    # Social metrics
    shares = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    
    # Conversion metrics
    contact_inquiries = models.PositiveIntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Analytics"
        verbose_name_plural = "Project Analytics"
        ordering = ['-total_views']

    def __str__(self):
        return f"Analytics for {self.project_title}"
