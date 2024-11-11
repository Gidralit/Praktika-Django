from tkinter.font import names

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
    path('applications/create-application', views.create_application_view, name='create-application'),
    path('applications/my-applications', views.show_applications_view, name='show-applications'),
    path('applications/delete-application/<int:application_id>/', views.delete_application_view, name='delete-application'),
    path('applications/edit-application/<int:application_id>/', views.edit_application_view, name='edit-application'),
]