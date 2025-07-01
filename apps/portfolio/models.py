from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """Main profile model for the portfolio owner"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume = models.FileField(upload_to='documents/', blank=True, null=True)
    
    # Contact Information
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    # Social Links
    github_url = models.URLField(blank=True, help_text="GitHub profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn profile URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter/X profile URL")
    facebook_url = models.URLField(blank=True, help_text="Facebook profile URL")
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text="Include country code, e.g., +263771234567")
    kaggle_url = models.URLField(blank=True, help_text="Kaggle profile URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    youtube_url = models.URLField(blank=True, help_text="YouTube channel URL")

    # Contact Information for Footer
    contact_email = models.EmailField(blank=True, help_text="Contact email for footer")
    contact_phone = models.CharField(max_length=20, blank=True, help_text="Contact phone for footer")
    contact_address = models.TextField(blank=True, help_text="Physical address for footer")
    business_hours = models.CharField(max_length=100, blank=True, help_text="e.g., Mon-Fri 9AM-5PM")

    # Additional Contact Links
    telegram_url = models.URLField(blank=True, help_text="Telegram contact URL")
    discord_url = models.URLField(blank=True, help_text="Discord server URL")
    skype_username = models.CharField(max_length=50, blank=True, help_text="Skype username")
    
    # SEO and Meta
    meta_description = models.TextField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.name


class ProfileImage(models.Model):
    """Multiple profile images for slideshow"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_images')
    image = models.ImageField(upload_to='profile_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', 'created_at']

    def __str__(self):
        return f"{self.profile.name} - Image {self.display_order}"


class Education(models.Model):
    """Education background model"""
    DEGREE_CHOICES = [
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    field_of_study = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Education"
        verbose_name_plural = "Education"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} - {self.institution}"


class Experience(models.Model):
    """Work experience model"""
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    technologies_used = models.TextField(blank=True, help_text="Comma-separated list of technologies")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.position} at {self.company}"

    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies_used:
            return [tech.strip() for tech in self.technologies_used.split(',')]
        return []


class Achievement(models.Model):
    """Achievements and awards model"""
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    date_received = models.DateField()
    description = models.TextField(blank=True)
    certificate_url = models.URLField(blank=True)
    certificate_image = models.ImageField(upload_to='achievements/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Achievement"
        verbose_name_plural = "Achievements"
        ordering = ['-date_received']

    def __str__(self):
        return self.title
