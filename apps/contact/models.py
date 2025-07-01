from django.db import models
from django.core.validators import RegexValidator


class ContactMessage(models.Model):
    """Contact form submissions"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Contact information
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20, 
        blank=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    company = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    
    # Message details
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Classification
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General Inquiry'),
            ('collaboration', 'Collaboration'),
            ('job_opportunity', 'Job Opportunity'),
            ('freelance', 'Freelance Project'),
            ('consultation', 'Consultation'),
            ('feedback', 'Feedback'),
            ('other', 'Other'),
        ],
        default='general'
    )
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        """Mark message as read"""
        if self.status == 'new':
            self.status = 'read'
            from django.utils import timezone
            self.read_at = timezone.now()
            self.save()

    def mark_as_replied(self):
        """Mark message as replied"""
        self.status = 'replied'
        from django.utils import timezone
        self.replied_at = timezone.now()
        self.save()


class NewsletterSubscription(models.Model):
    """Newsletter subscription model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Preferences
    interests = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated interests"
    )
    
    # Metadata
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, help_text="Where they subscribed from")
    
    # Timestamps
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(blank=True, null=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']

    def __str__(self):
        return f"{self.email} ({'Active' if self.is_active else 'Inactive'})"

    def get_interests_list(self):
        """Return interests as a list"""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',')]
        return []


class ContactFormSubmission(models.Model):
    """Track form submission analytics"""
    form_name = models.CharField(max_length=100)
    page_url = models.URLField()
    submission_data = models.JSONField()
    
    # Analytics
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(blank=True)
    session_id = models.CharField(max_length=100, blank=True)
    
    # Success tracking
    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Form Submission"
        verbose_name_plural = "Form Submissions"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.form_name} - {self.created_at.date()}"
