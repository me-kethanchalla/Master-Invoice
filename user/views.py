from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm
import random
from django.contrib.auth.decorators import login_required
import smtplib

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

def profile(request):
    return render(request, 'user/profile.html')

def edit_profile(request):
    """View to edit user profile"""
    user_profile = request.user.profile  # Fetch logged-in user's profile

    if request.method == "POST":
        firm_name = request.POST.get('firm_name')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Update the profile
        user_profile.firm_name = firm_name
        user_profile.full_name = full_name
        user_profile.phone = phone
        user_profile.address = address
        user_profile.save()

        # Update email in User model
        request.user.email = request.POST.get('email')
        request.user.save()

        messages.success(request, "Profile updated successfully!")  # Show success message
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'user/editprofile.html')
