from django.forms import ModelForm
from .models import Client
from django import forms

class UserRegistrationForm(ModelForm):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'id_number', 'email', 'date_of_birth']
        widgets = {
            'name': forms.TextInput(attrs={'type': 'text', 'placeholder': 'Enter your full names'}),
            'id_number': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter your ID number'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Enter your phone number'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }