from django.contrib.auth.models import AbstractUser
from django.db import models

# Extend the AbstractUser model to include custom fields
class User(AbstractUser):
    # Custom fields to extend the default User model
    contact = models.CharField(max_length=15, blank=True, null=True)  # New contact field
    pw = models.CharField(max_length=15, blank=True, null=True)  # New password field
    profilepicture = models.ImageField(upload_to='images/profilepictures', blank=True, null=True)  # Profile picture field

    # Modify related names to avoid clashes with Django's default User model
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

    def __str__(self):
        return f"{self.username} ({self.email}) ({self.pw}) "
