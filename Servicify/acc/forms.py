
from django import forms
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from .models import User, Serviceman, Booking


class UserForm(forms.ModelForm):
    """Customer sign up."""
    password = forms.CharField(
        widget=forms.PasswordInput, min_length=6,
        help_text='At least 6 characters.'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone', 'location', 'address']
        labels = {
            'location': 'Your area in Dhaka',
            'address': 'Address',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Select your area'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])  # hash it
        if commit:
            user.save()
        return user


class ServicemanForm(forms.ModelForm):
    """Service provider sign up."""
    password = forms.CharField(
        widget=forms.PasswordInput, min_length=6,
        help_text='At least 6 characters.'
    )

    class Meta:
        model = Serviceman
        fields = [
            'username', 'email', 'password', 'phone',
            'service', 'location', 'address', 'experience', 'bio'
        ]
        labels = {
            'service': 'Service you provide',
            'location': 'Area you work in',
            'experience': 'Experience (years)',
            'bio': 'About you',
        }
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Tell customers about your work (optional)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].empty_label = 'Select a service'
        self.fields['location'].empty_label = 'Select your area'

    def save(self, commit=True):
        provider = super().save(commit=False)
        provider.password = make_password(self.cleaned_data['password'])
        if commit:
            provider.save()
        return provider


class BookingForm(forms.ModelForm):
    """Customer books a provider."""

    class Meta:
        model = Booking
        fields = [
            'description', 'address', 'booking_date',
            'booking_time', 'offered_price'
        ]
        labels = {
            'description': 'What work do you need?',
            'address': 'Where should the work be done?',
            'booking_date': 'Date',
            'booking_time': 'Time',
            'offered_price': 'Price you can offer (BDT, optional)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'booking_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_booking_date(self):
        booking_date = self.cleaned_data['booking_date']
        if booking_date < timezone.localdate():
            raise forms.ValidationError('Please choose today or a future date.')
        return booking_date

    def clean_offered_price(self):
        price = self.cleaned_data.get('offered_price')
        if price is None:
            return 0
        if price < 0:
            raise forms.ValidationError('Price cannot be negative.')
        return price
