import re
from django.core.exceptions import ValidationError

def validator_cyrillic(value):
    if not re.match(r'^[а-яА-ЯёЁ\s-]+$', value):
        raise ValidationError('Введите только киррилические символы, пробелы, дефисы в вашем ФИО')

def validator_password(password1, password2):
    if password1 and password2 and password1 != password2:
        raise ValidationError('Ваши пароли не совпадают')

def validator_login(value):
    if not re.match(r'^[a-zA-Z\-]+$', value):
        raise ValidationError('В вашем логине должны быть только латинские буквы и дефисы')