
import sys
import random
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DetailsForm
from django.contrib.auth.decorators import login_required

def user_login(request):
    register_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                request.session['register_data'] = register_form.cleaned_data

                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['otp_expiry'] = str(datetime.datetime.now() + datetime.timedelta(minutes=1))  # 5-minute expiry
               
                print(f"OTP for : {otp}")
                sys.stdout.flush()
                return redirect('verify_otp') 
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
    user_profile = request.user.profile

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


        messages.success(request, "Profile updated successfully!")  # Show success message
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'user/editprofile.html')



@login_required
def details(request):
    """View for newly registered users to enter details"""

    # ✅ Ensure the user has a profile (it should already exist from registration)
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = DetailsForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Details saved successfully!")
            return redirect('home')
    else:
        form = DetailsForm(instance=user_profile)

    return render(request, 'user/profile_filing.html', {'form': form})

from django.utils.timezone import make_aware,now
from django.contrib.auth.models import User

def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        otp_expiry = request.session.get("otp_expiry")

        if otp_expiry:
           expiry_time = make_aware(datetime.datetime.fromisoformat(otp_expiry))
           if now() > expiry_time:
            messages.error(request, "OTP has expired. Please register again.")
            request.session.pop("register_data", None)  
            return redirect("register")  

        if str(user_otp) == str(stored_otp):
            user_data = request.session.get("register_data")
            if user_data:
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password1"]
                )
                login(request, user)
                Profile.objects.create(user=user)

                request.session.pop("register_data", None)
                request.session.pop("otp", None)
                request.session.pop("otp_expiry", None)

                messages.success(request, "Registration successful!")
                return redirect("details")

            messages.error(request, "Something went wrong. Please register again.")
            return redirect("register")
        
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")

    return render(request, "user/verify_otp.html")
