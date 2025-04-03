from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        }),
        help_text="Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only."
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'new-password'
        }),
        label="Password",
        help_text="Your password must contain at least 8 characters."
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password'
        }),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Add null checks before using len()
        if password1 is not None and password2 is not None:
            if password1 != password2:
                self.add_error('password2', "Passwords do not match!")
            if len(password1) < 8:
                self.add_error('password1', "Password must be at least 8 characters long.")
        else:
            self.add_error(None, "Password fields are required.")

        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Profile  # Ensure it's based on Profile model
        fields = ['firm_name', 'full_name', 'phone', 'address', 'GST_number']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firm_name', 'full_name', 'phone', 'address']
