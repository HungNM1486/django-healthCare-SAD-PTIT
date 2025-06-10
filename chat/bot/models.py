from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Chat session for {self.user.username} - {self.created_at}"

class Message(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=5, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.sender}: {self.content[:50]}"

class Intent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class TrainingPhrase(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='training_phrases')
    text = models.TextField()

    def __str__(self):
        return f"{self.text[:50]} - {self.intent.name}"

class Response(models.Model):
    intent = models.ForeignKey(Intent, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField()
    priority = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.text[:50]} - {self.intent.name}"