from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    surname = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    patronym = models.CharField(max_length=20)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username

# Create your models here.
