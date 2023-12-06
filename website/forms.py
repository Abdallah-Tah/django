# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Record

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Email Address'})
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Last Name'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Password'}),
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$',
                message=_("The password must contain at least 8 characters, one letter, one number, and one special character."),
            ),
        ]
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("A user with that email already exists."))
        return email

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Username'})
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Password'})
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Confirm Password'})
        self.fields['password2'].label = ''

class AddRecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Phone'}),
            'address': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'State'}),
            'zipcode': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Zip Code'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Email'}),
        }

        
