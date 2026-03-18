from django.forms import ModelForm
from django import forms
from .models import Contract, Player

class PlayerRegisterForm(ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Player
        fields = ['name', 'email', 'date_of_birth', 'phone_number','id_no','skills','coach','player_position','club_before','current_club','activity']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'placeholder': 'Enter phone number'}),
            'id_no': forms.TextInput(attrs={'type': 'number', 'placeholder': "Enter your ID number"}),
            'skills': forms.CheckboxSelectMultiple(),
            'player_position': forms.CheckboxSelectMultiple(),

        }