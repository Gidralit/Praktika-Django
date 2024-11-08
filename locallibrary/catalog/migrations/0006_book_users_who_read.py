# Generated by Django 3.2.25 on 2024-11-08 06:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0005_auto_20241108_1224'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='users_who_read',
            field=models.ManyToManyField(blank=True, related_name='read_book', to=settings.AUTH_USER_MODEL),
        ),
    ]
