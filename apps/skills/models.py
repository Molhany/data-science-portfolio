from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SkillCategory(models.Model):
    """Categories for organizing skills"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, default="#007bff", help_text="Hex color code")
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Skill(models.Model):
    """Individual skills model"""
    PROFICIENCY_CHOICES = [
        (1, 'Beginner'),
        (2, 'Basic'),
        (3, 'Intermediate'),
        (4, 'Advanced'),
        (5, 'Expert'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    proficiency_level = models.IntegerField(
        choices=PROFICIENCY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3
    )
    years_of_experience = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    description = models.TextField(blank=True)
    
    # Visual elements
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, blank=True, help_text="Hex color code")
    
    # Certifications and validation
    is_certified = models.BooleanField(default=False)
    certification_name = models.CharField(max_length=200, blank=True)
    certification_url = models.URLField(blank=True)
    certification_date = models.DateField(blank=True, null=True)
    
    # Display options
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['category', 'display_order', '-proficiency_level', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.get_proficiency_level_display()})"

    def get_proficiency_percentage(self):
        """Return proficiency as percentage for progress bars"""
        return (self.proficiency_level / 5) * 100

    def get_proficiency_stars(self):
        """Return proficiency as star rating"""
        return '★' * self.proficiency_level + '☆' * (5 - self.proficiency_level)


class SkillEndorsement(models.Model):
    """Endorsements for skills (like LinkedIn endorsements)"""
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='endorsements')
    endorser_name = models.CharField(max_length=100)
    endorser_title = models.CharField(max_length=200, blank=True)
    endorser_company = models.CharField(max_length=200, blank=True)
    endorser_linkedin = models.URLField(blank=True)
    endorsement_text = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Skill Endorsement"
        verbose_name_plural = "Skill Endorsements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.endorser_name} endorses {self.skill.name}"


class SkillProgress(models.Model):
    """Track skill progress over time"""
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='progress_history')
    proficiency_level = models.IntegerField(
        choices=Skill.PROFICIENCY_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    notes = models.TextField(blank=True)
    milestone_achieved = models.CharField(max_length=200, blank=True)
    
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Skill Progress"
        verbose_name_plural = "Skill Progress Records"
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.skill.name} - Level {self.proficiency_level} ({self.recorded_at.date()})"
