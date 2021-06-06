from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from account.models import Account


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

        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'bobsmith@gmail.com', })
        self.fields['password1'].widget.attrs.update({'class': 'input', 'placeholder': '*******'})
        self.fields['password2'].widget.attrs.update({'class': 'input', 'placeholder': '*******'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Danis'}),
            'last_name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Zinnatullin'}),
            'username': forms.HiddenInput(attrs={'help_text': '', }),
        }

    def clean_password(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError('''Passwords don\'t match.''')

        return cd['password2']


class UserSignInForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserSignInForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'input', 'placeholder': 'bobsmith@gmail.com', 'id': 'id_username',
               'autocomplete': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'input', 'placeholder': '*******', 'id': 'id_password', 'autocomplete': 'current-password'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['photo']
        exclude = ['user', 'is_verified', 'verification_uuid']
