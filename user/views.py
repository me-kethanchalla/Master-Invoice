import sys
import os
import secrets
import hashlib
import datetime
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DetailsForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.cache import never_cache

# OTP
def generate_secure_otp(length=6):
    return ''.join(str(secrets.randbelow(10)) for _ in range(length))
# Hash the OTP using SHA-256
def hash_otp(otp):
    return hashlib.sha256(otp.encode()).hexdigest()
#OTP storage
def store_otp(request, otp, expiry_minutes=5):
    request.session['otp'] = hash_otp(otp)
    request.session['otp_expiry'] = str(datetime.datetime.now() + datetime.timedelta(minutes=expiry_minutes))
    request.session.modified = True
#otp email 
def send_otp_email(to_email, otp):
    """Send an OTP via email."""
    subject = "Your OTP Code"
    message = f"Your One-Time Password (OTP) is: {otp}"
    from_email = 'master.invoice.while1@gmail.com'  # Replace with your email address

    try:
        send_mail(subject, message, from_email, [to_email])
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

#user login
def user_login(request):
    register_form = CustomUserCreationForm()
    login_form = CustomAuthenticationForm()

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = CustomUserCreationForm(request.POST)
            if register_form.is_valid():
                request.session['register_data'] = register_form.cleaned_data

                otp = generate_secure_otp()
                store_otp(request, otp, 5)
                send_otp_email(register_form.cleaned_data['email'], otp) 
                return redirect('verify_otp')   
            # else:
            #     messages.error(request, "Registration failed. Please check the errors below.")

        elif 'login' in request.POST:
            login_form = CustomAuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
               # messages.success(request, "Login successful.")
                return redirect('home')
            # else:
            #     messages.error(request, "Login failed. Please check your credentials.")    
    return render(request, 'user/login.html',{
        'register_form': register_form,
        'login_form': login_form
    })

@login_required(login_url='/')
@never_cache
def home(request):
    return render(request, 'user/welcome.html')

def profile(request):
    return render(request, 'user/profile.html')

#edit profile 
def edit_profile(request):
    user_profile = request.user.profile

    if request.method == "POST":
        firm_name = request.POST.get('firm_name')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        user_profile.firm_name = firm_name
        user_profile.full_name = full_name
        user_profile.phone = phone
        user_profile.address = address
        user_profile.save()

       # messages.success(request, "Profile updated successfully!")  # Show success message
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'user/editprofile.html')



@login_required
def details(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile_form = DetailsForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
          #  messages.success(request, "Details saved successfully!")
            return redirect('home')
        
    else:
        profile_form = DetailsForm(instance=user_profile)

    return render(request, 'user/profile_filing.html')




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

        if str(hash_otp(user_otp)) == str(stored_otp):
            user_data = request.session.get("register_data")
            if user_data:
                user = User.objects.create_user(
                    username=user_data["username"],
                    email=user_data["email"],
                    password=user_data["password1"]
                )
                login(request, user)
                 
                request.session.pop("register_data", None)
                request.session.pop("otp", None)
                request.session.pop("otp_expiry", None)
                
                return redirect("details")
            else:
                messages.error(request, "No registration data found. Please try again.")
                return redirect("register")
        
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect("verify_otp")
    return render(request, "user/verify_otp.html")



def resend_otp(request):
    if request.method == "POST":
        user_data = request.session.get("register_data")
        if user_data:
            otp = generate_secure_otp()  # Generate new OTP
            store_otp(request, otp, 5)  # Store OTP in session with a 5-minute expiry
            send_otp_email(user_data["email"], otp)  # Send OTP via email
            return JsonResponse({"message": "OTP resent successfully!"}, status=200)
        else:
            return JsonResponse({"error": "No registration data found. Please register again."}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.contrib.auth import logout

@never_cache
def user_logout(request):
    logout(request)
#    messages.success(request, "Logged out successfully.")
    request.session.flush()  # Clears all session data
    return redirect('login2')



def send_verify_mail(email,request):
    otp=generate_secure_otp()
    store_otp(request, otp, 5) 
    send_otp_email(email, otp)  # Send OTP via email


def verify_and_reset(request):
    email = request.session.get('reset_email')

    if not email:
        return redirect('reset_password')  # Redirect if session expires

    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        new_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        stored_otp =  request.session.get("otp")
        entered_otp = hash_otp(entered_otp)
        if stored_otp and entered_otp == stored_otp:
            if new_password == confirm_password:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                request.session.pop("otp", None)
                request.session.pop("otp_expiry", None) 
                # messages.success(request, "Password reset successful. You can now log in.")
                return redirect('login2')
            else:
                messages.error(request, "Passwords do not match.")
        else:
            messages.error(request, "Invalid OTP.")

    return render(request, "user/verify_reset.html")

def request_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            send_verify_mail(email,request=request)  # Send OTP to email
            messages.success(request, "An OTP has been sent to your email for verification.")
            request.session['reset_email'] = email  # Store email in session
            return redirect('verify_reset')  # Redirect to OTP & password page
        else:
            messages.error(request, "No user with this Email")

    return render(request, "user/forgot_password.html")

    

# views.py
from django.conf import settings
from django.http import JsonResponse

def db_info(request):
    db_settings = settings.DATABASES.get('default', {})
    engine = db_settings.get('ENGINE', 'Not Found')
    return JsonResponse({'database_engine': engine})
