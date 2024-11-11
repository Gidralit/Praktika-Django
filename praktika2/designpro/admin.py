from django.contrib import admin
from .models import CustomUser, Categories, Application

admin.site.register(CustomUser)
admin.site.register(Categories)
admin.site.register(Application)
# Register your models here.
