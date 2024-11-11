from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey


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
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(upload_to='photos/', blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title
# Create your models here.
