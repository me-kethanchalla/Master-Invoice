import secrets
import hashlib
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import Profile
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DetailsForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

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
    from_email = 'maste.invoice253@gmail.com'  # Replace with your email address

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
    return render(request, 'user/login.html',{
        'register_form': register_form,
        'login_form': login_form
    })


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

        messages.success(request, "Profile updated successfully!")  # Show success message
        return redirect('profile')  # Redirect to profile page after saving

    return render(request, 'user/editprofile.html')



@login_required
def details(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        profile_form = DetailsForm(request.POST, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Details saved successfully!")
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
#resend OTP....
    return render(request, "user/verify_otp.html")
