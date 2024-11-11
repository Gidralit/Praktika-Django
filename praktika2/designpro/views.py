from audioop import reverse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegistrationForm
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

# Create your views here.
