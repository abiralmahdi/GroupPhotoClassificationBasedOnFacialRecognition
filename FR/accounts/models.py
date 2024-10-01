from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# User model extending Django's AbstractUser to include username, email, and password
class User(AbstractUser):
    # Other custom fields here
    # Add unique related_name to avoid clashes with the default auth user
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Change related_name to something unique
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Change related_name to something unique
        blank=True
    )
    profilepicture = models.ImageField(upload_to='images/profilepictures')
