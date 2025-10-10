from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .models import UserMessage
from captcha.fields import CaptchaField, CaptchaTextInput

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your username or email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

    
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("This email already in use!")
        return email


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(label='', disabled=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter your username'}))
    email = forms.EmailField(label='', disabled=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter your old password'}))
    new_password1 =  forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Enter new password'}))
    new_password2 =  forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your new password'}))


class ContactUsForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'placeholder': 'Enter the text shown'}))

    class Meta:
        model = UserMessage
        fields = ['full_name', 'email', 'comment']
        widgets = {'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
                   'comment': forms.Textarea(attrs={'placeholder': 'Your comment'})}   
        
