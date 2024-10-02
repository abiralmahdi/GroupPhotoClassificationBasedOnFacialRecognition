from django.db import models
from accounts.models import User
from django.conf import settings


# Picture model where each picture is uploaded by a user (ForeignKey to User)
class Picture(models.Model):
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey to User
    image = models.ImageField(upload_to='images/')
    image_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Image {self.image_id} uploaded by {self.uploader.username}"


class Event(models.Model):
    name = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=1000, default="")
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_events', default="") 
    guests = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='guest_events')
    event_date = models.DateField(default="")
    eventPic = models.ImageField(upload_to='images/eventPictures', blank=True, null=True)

    def __str__(self):
        return f"Event {self.name} hosted by {self.host.username}"


# PicsRelation model to relate a picture to a user (ForeignKey to Picture and User)
class PicsRelation(models.Model):
    pic = models.ForeignKey(Picture, on_delete=models.CASCADE)  # ForeignKey to Picture
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey to User (aid)
    
    def __str__(self):
        return f"Relation between {self.pic.image_id} and user {self.user.username}"
