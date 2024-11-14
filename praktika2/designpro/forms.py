import os.path
from cProfile import label

from django.core.exceptions import ValidationError
from django import forms
from django.db.transaction import clean_savepoints

from .models import CustomUser, Application, Categories
from .validators import validator_cyrillic, validator_password, validator_login

class SearchForm(forms.Form):
    query = forms.CharField(label = 'Поиск', max_length=100, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Введите текст для поиска...',
    }))
    start_date = forms.DateField(label='Дата начала', required=False, widget=forms.DateInput(attrs={
        'type':'date',
    }))
    end_date = forms.DateField(label='Дата окончания', required=False, widget=forms.DateInput(attrs={
        'type': 'date',
    }))

class ApplicationForm(forms.ModelForm):
    # comment = forms.CharField(required=False)
    # additional_photo = forms.ImageField(required=False)

    class Meta:
        model = Application
        fields = [
            'title',
            'description',
            'category',
            'photo',
            'start_date',
            'end_date',
            # 'additional_photo',
            # 'comment',
        ]


    def clean(self):
        cleaned_data = super().clean()

        photo = cleaned_data.get('photo')
        if photo is None:
            raise forms.ValidationError('Загрузите файл изображения')

        if photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Ваше изображение слишком большое, максимальный размер 2МБ')

        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        ext = os.path.splitext(photo.name)[1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError('Недопустимое расширение файла. Поддерживаемые форматы: .jpg, .jpeg, .png, .bmp')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)


class EditStatusForm(forms.ModelForm):
    status = forms.ChoiceField(choices=Application.STATUS_CHOICES)
    additional_photo = forms.ImageField(required=False)
    comment = forms.CharField(required=False)
    class Meta:
        model = Application
        fields = ['status', 'additional_photo', 'comment']

    def __init__(self, *args, user=None, **kwargs):
        super(EditStatusForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        comment = cleaned_data.get('comment')

        if status == 'in_progress' and not comment:
            raise forms.ValidationError('Комментарий обяязателен если вы отправляете заявку на доработку')

        return cleaned_data

class EditUserApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'photo', 'start_date', 'end_date', 'category']


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

class CategoriesForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name']
        labels = {
            'name': 'Название категории'
        }


