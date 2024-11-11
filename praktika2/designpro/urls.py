from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('authentication/register/', views.register_view, name='register'),
    path('authentication/login/', views.CustomLoginView.as_view(), name='login'),
    path('authentication/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('profile/profile/', views.profile_view, name='profile'),
    path('home/', views.home_view, name='home'),
    path('captcha/', include('captcha.urls')),
]