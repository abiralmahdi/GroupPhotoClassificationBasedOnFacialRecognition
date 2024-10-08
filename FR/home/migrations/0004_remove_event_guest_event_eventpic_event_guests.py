# Generated by Django 5.0.4 on 2024-10-02 21:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_remove_event_event_id_event_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='guest',
        ),
        migrations.AddField(
            model_name='event',
            name='eventPic',
            field=models.ImageField(blank=True, null=True, upload_to='images/eventPictures'),
        ),
        migrations.AddField(
            model_name='event',
            name='guests',
            field=models.ManyToManyField(related_name='guest_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
