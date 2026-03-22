from django.forms import ModelForm
from .models import Admin, Client, Item
from django import forms

class ClientRegistrationForm(ModelForm):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'id_no', 'date_of_birth']
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Enter your phone number...'}),
            'id_no': forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter your ID number'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }

class ItemUpdateForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category','action', 'quantity','discount', 'buying_price', 'selling_price']
       

class ItemCreationForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'action', 'quantity','discount', 'category', 'buying_price', 'selling_price']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter item name'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'discount': forms.NumberInput(attrs={'placeholder': 'Enter discount %'}),
            'buying_price': forms.NumberInput(attrs={'placeholder': 'Buying price'}),
            'selling_price': forms.NumberInput(attrs={'placeholder': 'Selling price'}),
        }
