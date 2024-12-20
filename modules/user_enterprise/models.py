from django.db import models
from modules.user.models import User  
from modules.enterprise.models import Enterprise  

class UserEnterprise(models.Model):
    ue_id = models.AutoField(primary_key=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_enterprises")
    
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name="enterprise_users")
    
    role = models.CharField(max_length=50)

    class Meta:
        verbose_name = "User Enterprise"
        verbose_name_plural = "User Enterprises"
        db_table = "user_enterprise"

    def __str__(self):
        return f"{self.user.username} - {self.enterprise.name} - {self.role}"
