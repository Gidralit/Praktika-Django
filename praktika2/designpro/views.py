from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

def home(request):
    return redirect('home')

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
        form = RegistrationForm()
    return render(request, 'authentication/register.html', {'user_form': form})

def profile_view(request):
    return render(request, 'profile/profile.html', )

# Create your views here.
