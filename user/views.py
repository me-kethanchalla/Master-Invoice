# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def login(request):
    if request.method == 'POST':
        if 'register' in request.POST:  # Register form submitted
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # Redirect to login page after successful registration
        elif 'login' in request.POST:  # Login form submitted
            form = CustomAuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                # login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        register_form = CustomUserCreationForm()
        login_form = CustomAuthenticationForm()

    return render(request, 'user/login.html', {
        'register_form': register_form,
        'login_form': login_form })

def welcome(request):
    return render(request, 'user/welcome.html')

