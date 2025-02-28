# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def user_login(request):
    register_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                return redirect('login')  
        elif 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('home')  

    return render(request, 'registration/login.html', {
        'register_form': register_form,
        'login_form': login_form
    })

def home(request):
    return render(request, 'registration/home.html')

