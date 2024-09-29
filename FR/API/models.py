from django.db import models
from django.contrib.auth.models import AbstractUser


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

# Picture model where each picture is uploaded by a user (ForeignKey to User)
class Picture(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User
    image = models.ImageField(upload_to='images/')
    image_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Image {self.image_id} uploaded by {self.uploader.username}"

# Event model where each event is linked to a guest (ForeignKey to User)
from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_events', default="")  # Default user ID
    event_id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_events', default="")
    event_date = models.DateField()

    def __str__(self):
        return f"Event {self.event_id} hosted by {self.host.username} for guest {self.guest.username}"


# PicsRelation model to relate a picture to a user (ForeignKey to Picture and User)
class PicsRelation(models.Model):
    pic = models.ForeignKey(Picture, on_delete=models.CASCADE)  # ForeignKey to Picture
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User (aid)
    
    def __str__(self):
        return f"Relation between {self.pic.image_id} and user {self.user.username}"
