# Generated by Django 5.0.4 on 2024-11-07 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_event_description_alter_event_host_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]