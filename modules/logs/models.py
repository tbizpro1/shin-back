from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Log(models.Model):
    CHANGE_TYPE_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('read', 'Read'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs")
    description = models.TextField()
    change_type = models.CharField(max_length=10, choices=CHANGE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log: {self.user} - {self.change_type}"
