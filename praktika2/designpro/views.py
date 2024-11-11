from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegistrationForm, ApplicationForm
from .models import Categories, Application

from django.contrib.auth.views import LoginView, LogoutView
import random

def home(request):
    return redirect('home')

class CustomLogoutView(LogoutView):
    def get_success_url(self):
        messages.success(self.request, 'Вы успешно вышли из аккаунта')
        return reverse_lazy('home')

class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'

    def form_valid(self, form):
        user = form.get_user()
        if user.is_banned:
            messages.error(self.request, 'К сожалению вы забанены( плаки плаки((')
            return redirect('register')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile')

def home_view(request):
    return render(request, 'pages/home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'user_form': form})

def profile_view(request):
    return render(request, 'profile/profile.html', )

@login_required
def create_application_view(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            print(f'форма: {form}')
            print(application)
            application.user = request.user
            application.save()
            messages.success(request, 'Вы успешно оставили заявку')
            return redirect('home')
        else:
            print('Форма не валидна')
    else:
        form = ApplicationForm()
    return render(request, 'applications/create_application.html', {'form': form})

@login_required
def show_applications_view(request):
    applications = Application.objects.filter(user=request.user).all()
    return render(request, 'applications/show_applications.html', {'applications': applications})

@login_required
def delete_application_view(request):
    application = get_object_or_404(Application, id = request.application.id, user=request.user)

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Ваша заявка успешно удалена')

# Create your views here.
