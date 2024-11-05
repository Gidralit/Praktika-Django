from django.urls import path
from . import urls, views

urlpatterns = [
    path('', views.index, name='index'),
]