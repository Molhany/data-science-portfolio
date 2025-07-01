from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatSession(models.Model):
    """Chat session model"""
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    visitor_name = models.CharField(max_length=100, blank=True)
    visitor_email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Chat {self.session_id} - {self.visitor_name or 'Anonymous'}"


class ChatMessage(models.Model):
    """Chat message model"""
    MESSAGE_TYPES = [
        ('user', 'User'),
        ('bot', 'Bot'),
        ('system', 'System'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}..."


class ChatBotResponse(models.Model):
    """Predefined chatbot responses"""
    TRIGGER_TYPES = [
        ('keyword', 'Keyword'),
        ('intent', 'Intent'),
        ('greeting', 'Greeting'),
        ('fallback', 'Fallback'),
    ]
    
    trigger_type = models.CharField(max_length=20, choices=TRIGGER_TYPES)
    trigger_text = models.CharField(max_length=200, help_text="Keywords or phrases that trigger this response")
    response_text = models.TextField()
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher priority responses are checked first")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'trigger_text']

    def __str__(self):
        return f"{self.trigger_type}: {self.trigger_text}"
