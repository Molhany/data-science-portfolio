from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class ProjectCategory(models.Model):
    """Categories for organizing projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Category"
        verbose_name_plural = "Project Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Technology(models.Model):
    """Technologies used in projects"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class or image URL")
    color = models.CharField(max_length=7, default="#6c757d", help_text="Hex color code")
    website_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """Main project model"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    
    # Project details
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE, related_name='projects')
    technologies = models.ManyToManyField(Technology, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # Media
    featured_image = models.ImageField(upload_to='projects/featured/', blank=True, null=True)
    demo_video = models.FileField(upload_to='projects/videos/', blank=True, null=True)
    
    # Links
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    
    # Project metrics
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    duration_hours = models.PositiveIntegerField(blank=True, null=True, help_text="Estimated hours spent")
    
    # Features and highlights
    key_features = models.TextField(blank=True, help_text="One feature per line")
    challenges_faced = models.TextField(blank=True)
    lessons_learned = models.TextField(blank=True)
    
    # Display options
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-is_featured', 'display_order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})

    def get_key_features_list(self):
        """Return key features as a list"""
        if self.key_features:
            return [feature.strip() for feature in self.key_features.split('\n') if feature.strip()]
        return []

    def get_duration_display(self):
        """Return human-readable duration"""
        if self.duration_hours:
            if self.duration_hours < 24:
                return f"{self.duration_hours} hours"
            else:
                days = self.duration_hours // 24
                remaining_hours = self.duration_hours % 24
                if remaining_hours:
                    return f"{days} days, {remaining_hours} hours"
                return f"{days} days"
        return "Duration not specified"


class ProjectImage(models.Model):
    """Additional images for projects"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"{self.project.title} - Image {self.display_order}"


class ProjectLink(models.Model):
    """Additional links for projects"""
    LINK_TYPES = [
        ('github', 'GitHub Repository'),
        ('demo', 'Live Demo'),
        ('documentation', 'Documentation'),
        ('article', 'Article/Blog Post'),
        ('video', 'Video Tutorial'),
        ('dataset', 'Dataset'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='additional_links')
    title = models.CharField(max_length=100)
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='other')
    description = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Project Link"
        verbose_name_plural = "Project Links"
        ordering = ['link_type', 'title']

    def __str__(self):
        return f"{self.project.title} - {self.title}"
