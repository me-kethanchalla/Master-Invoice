from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def login(request):
    # Define default forms first
    register_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:  # Register form submitted
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                return redirect('login')  # Redirect to login page after successful registration
        elif 'login' in request.POST:  # Login form submitted
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)  # Log the user in!
                return redirect('home')  # Redirect to home page after successful login

    return render(request, 'user/login.html', {
        'register_form': register_form,
        'login_form': login_form
    })


def welcome(request):
    return render(request, 'user/welcome.html')


