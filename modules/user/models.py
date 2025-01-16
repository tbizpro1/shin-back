from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=11, null=True, blank=True, default='')
    linkedin = models.CharField(max_length=255, null=True, blank=True, default='')
    profession = models.CharField(max_length=128, null=True, blank=True, default='')
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='user', null=True, blank=True)
    profile_picture = models.URLField(max_length=255)
    
    REQUIRED_FIELDS = ['password', 'username']
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return f'{self.username} - {self.email}'
    
    