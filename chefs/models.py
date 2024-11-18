# accounts/models.py
from django.contrib.auth.models import AbstractUser 
from django.db import models

class CustomUser(AbstractUser):
    EXPERIENCE_LEVEL = [
        ('CB', 'Chef Beginner'),
        ('CI', 'Chef Intermediate'),
        ('CA', 'Chef Advanced'),
        ('CM', 'Chef Master'),
    ]
    experience = models.CharField(max_length=2, choices=EXPERIENCE_LEVEL, default='CB')
    bio = models.CharField(max_length=400)
    favoriteCuisine = models.CharField(max_length=50)