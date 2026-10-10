
from django import forms
from .models import User, Serviceman


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'address']
        widgets = {
            'password': forms.PasswordInput()
        }


class ServicemanForm(forms.ModelForm):
    class Meta:
        model = Serviceman
        fields = [
            'username', 'email', 'password', 'phone', 'address',
            'service_name', 'experience'
        ]
        widgets = {
            'password': forms.PasswordInput()
        }