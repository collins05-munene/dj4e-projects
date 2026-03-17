from django.forms import ModelForm
from django import forms
from .models import Contract, Player

class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = ['contract_start', "contract_end", 'salary']
        widgets = {
            'contract_start': forms.DateInput(attrs={'type': 'date'}),
            'contract_end': forms.DateInput(attrs={'type': 'date'}),
            'salary': forms.NumberInput(attrs={'step': '0.01'}),
        }
        
class PlayerForm(ModelForm):
    class Meta:
        model = Player
        exclude = ['contract', 'created-at']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'player@gmail.com'}),
            'phone_number': forms.TextInput(attrs={'type': 'tel', 'pattern': '[0-9]{10}'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'id_no': forms.TextInput(attrs={'max_length': '8'})
        }