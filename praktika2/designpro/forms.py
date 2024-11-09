from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django import forms

from .models import CustomUser
from .validators import validator_cyrillic, validator_password, validator_login

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = [
            'surname',
            'name',
            'patronym',
            'username',
            'email',
            'password1',
            'password2',
            'is_data_processing_accepted',
        ]
        labels = {
            'surname': 'Фамилия',
            'name': 'Имя',
            'patronym': 'Отчество',
            'username': 'Логин',
            'email': 'Почта',
        }

    def clean(self):
        cleaned_data = super().clean()
        surname = cleaned_data.get('surname')
        name = cleaned_data.get('name')
        patronym = cleaned_data.get('patronym')
        username = cleaned_data.get('username')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        accepted = cleaned_data.get('is_data_processing_accepted')
        if surname:
            validator_cyrillic(surname)
        if name:
            validator_cyrillic(name)
        if patronym:
            validator_cyrillic(patronym)
        if username:
            validator_login(username)
        if password1 and password2:
            validator_password(password1, password2)
        if not accepted:
            raise ValidationError('Вы должны согласиться на обработку персональных данных')

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

