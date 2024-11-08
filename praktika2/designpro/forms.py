from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django import forms

from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    pass
    class Meta:
        model = CustomUser
        fields = ['surname', 'name', 'patronym', 'username', 'email', 'password1', 'password2']
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'patronym': 'Отчество',
            'username': 'Логин',
            'email': 'Почта',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
