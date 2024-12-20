from django.db import models
from modules.user.models import User  
from modules.enterprise.models import Enterprise  

class UserEnterprise(models.Model):
    ue_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_enterprises")
    
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="enterprise_users")
    
    role = models.CharField(max_length=50)

    INVITATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    status = models.CharField(
        max_length=20, 
        choices=INVITATION_STATUS_CHOICES, 
        default='pending', 
        verbose_name="Invitation Status"
    )

    class Meta:
        verbose_name = "User Enterprise"
        verbose_name_plural = "User Enterprises"
        db_table = "user_enterprise"

    def __str__(self):
        return f"{self.user.username} - {self.enterprise.name} - {self.role} ({self.status})"
