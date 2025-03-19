from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def user_login(request):
    register_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        # Check which form is submitted by looking at the button name.
        if 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Registration successful. Please log in.")
                return redirect('login2')
            else:
                messages.error(request, "Registration failed. Please check the errors below.")
        elif 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Login failed. Please check your credentials.")
    
    return render(request, 'user/login.html', {
        'register_form': register_form,
        'login_form': login_form
    })

def home(request):
    return render(request, 'user/welcome.html')
