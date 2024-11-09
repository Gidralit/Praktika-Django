from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('authentication/register/', views.register_view, name='register'),
    path('authentication/login/', LoginView.as_view(template_name='authentication/login.html'), name='login'),
    path('authentication/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home')
]