from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['email'].help_text = ''
        self.fields['first_name'].help_text = ''
        self.fields['last_name'].help_text = ''

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('''Passwords don\'t match.''')

        return cd['password2']


class UserSignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
