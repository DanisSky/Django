from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your name'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your surname'}),
            'email': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your email'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your address'}),
            'postal_code': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your code'}),
            'city': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your city'}),

        }
