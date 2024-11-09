from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django import forms
from captcha.fields import CaptchaField

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from .models import CustomUser
from .validators import validator_cyrillic, validator_password, validator_login

import base64
import random


class MathCapcthaField(CaptchaField):

    def __init__(self, *args, **kwargs):
        self.question, self.answer = self.generate_question()
        kwargs['label'] = self.question
        super().__init__(*args, **kwargs)

    def generate_question(self):
        operations = ['+', '-', '*']
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(operations)

        question = ''
        answer = None

        if operation == '+':
            question = f'{num1} + {num2}'
            answer = num1 + num2
        elif operation == '-':
            question = f'{num1} - {num2}'
            answer = num1 - num2
        elif operation == '*':
            question = f'{num1} * {num2}'
            answer = num1*num2

        return question, answer

    def generate_image(self, question):
        font = ImageFont.truetype('arial.ttf', size=40)
        image = Image.new('RGB', (200, 100), color=(255, 255, 255))
        draw = ImageDraw.Draw(image)
        text_size = draw.textsize(question, font=font)
        draw.text(((200-text_size[0]) / 2, (100 - text_size[1]) / 2), question, font=font, fill=(0, 0, 0))

        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        img_str = base64.b64encode(buffer.read()).decode('utf-8')

        return f'data:image/png;base64,{img_str}'

    def get_image_tag(self, image_base64):
        return f'<img src="{image_base64}" alt="captcha" style="border: 1px solid #000;" />'



    def clean(self, value):
        super().clean(value)
        if value != str(self.answer):
            raise ValidationError('Неверный ответ на капчу')

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    captcha = MathCapcthaField()
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

        captcha_value = cleaned_data.get('captcha')
        if not captcha_value:
            raise ValidationError('Ошибка при вводе капчи, повторите попытку')

        return cleaned_data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


