from email.policy import default

from PIL.ImageFont import truetype
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.cache.backends.base import default_key_func
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import ForeignKey, CASCADE

from datetime import datetime


class CustomUser(AbstractUser):
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronym = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    is_data_processing_accepted = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Categories(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):
    STATUS_CHOICES = [
        ('accepted_to_work', 'Принято в работу'),
        ('done', 'Выполнено'),
        ('new', 'Новая'),
        ('in_progress', 'На доработке'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = ForeignKey(Categories, on_delete=CASCADE, null=True)
    photo = models.ImageField(upload_to='photos/', blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    additional_photo = models.ImageField(upload_to='additional_photo/', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                raise ValidationError('Дата окончания не может быть раньше даты начала')
            elif self.start_date > self.end_date:
                raise ValidationError('Дата начала не может быть позже даты конца')


# Create your models here.
