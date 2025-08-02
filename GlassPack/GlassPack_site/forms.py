from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.forms import widgets
from .models import UserMessage

class ContactUsForm(forms.ModelForm):
    captcha = CaptchaField(widget=CaptchaTextInput(attrs={'placeholder': 'Enter the text shown'})
    )
    class Meta:
        model = UserMessage
        fields = ['full_name', 'email', 'comment']
        widgets = {'full_name': forms.TextInput(attrs={'placeholder': 'Your Full Name'}),
                   'email': forms.EmailInput(attrs={'placeholder': 'Your Email'}),
                   'comment': forms.Textarea(attrs={'placeholder': 'Your comment'})}
