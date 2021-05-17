from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(UserSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['username'].required = False
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['last_name'].help_text = ''

        self.fields['email'].widget.attrs.update({'class': 'login__input'})
        self.fields['password1'].widget.attrs.update({'class': 'login__input'})
        self.fields['password2'].widget.attrs.update({'class': 'login__input'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'login__input', 'placeholder': 'Last name'}),
            'username': forms.HiddenInput(attrs={'help_text': '', }),
        }

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('''Passwords don\'t match.''')

        return cd['password2']


class UserSignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'login__input'}),
            'password': forms.PasswordInput(attrs={'class': 'login__input'}),
        }
