from audioop import reverse
from turtledemo.penrose import start

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy

from .forms import RegistrationForm, ApplicationForm, SearchForm
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
            application.user = request.user
            application.status = 'new'
            application.save()
            messages.success(request, 'Вы успешно оставили заявку')
            return redirect('home')
    else:
        form = ApplicationForm(user=request.user)
    return render(request, 'applications/create_application.html', {'form': form})

@login_required
def show_applications_view(request):
    form = SearchForm(request.GET or None)

    if request.user.is_staff:
        applications = Application.objects.all()
    else:
        applications = Application.objects.filter(user=request.user).all()

    search_query = request.GET.get('query', '')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if query:
            applications = applications.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        if start_date:
            applications = applications.filter(start_date__gte=start_date)
        if end_date:
            applications = applications.filter(end_date__lte=end_date)

    return render(request, 'applications/show_applications.html', {'applications': applications, 'form': form, 'search_query': search_query})

@login_required
def delete_application_view(request, application_id):
    application = get_object_or_404(Application, id = application_id, user=request.user)

    if request.method == 'POST':
        application.delete()
        messages.success(request, 'Ваша заявка успешно удалена')
        return redirect('home')
    return render(request, 'applications/delete_application.html', {"application": application })

@login_required
def edit_application_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES, instance=application, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            if request.user.is_staff:
                application.status = form.cleaned_data.get('status')
            application.save()
            messages.success(request, 'Вы успешно изменили заявку')
            return redirect('home')
    else:
        form = ApplicationForm(instance=application, user=request.user)

    return render(request, 'applications/edit_application.html', {'form': form, 'application': application})

# Create your views here.
