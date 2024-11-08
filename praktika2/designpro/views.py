from django.shortcuts import render
from .forms import RegistrationForm

def home(request):
    return render(request, 'index.html')

def register(request):
    user_form = RegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})

# Create your views here.
