# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Username'})
        self.fields['username'].label = ''
        self.fields['password1'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Password'})
        self.fields['password1'].label = ''
        self.fields['password2'].widget.attrs.update({'class': 'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder': 'Confirm Password'})
        self.fields['password2'].label = ''

class AddRecordForm(forms.ModelForm):
    # Override the default init method to add a placeholder attribute to each field
    first_name = forms.CharField(
        required=True,
        widget=forms.widgets.TextInput(attrs={"placeholder": "First Name", "class": "block w-full px-4 py-2 mt-1 border rounded-md"}),
        label=""
    )
    last_name = forms.CharField(
        required=True,
		widget=forms.widgets.TextInput(attrs={"placeholder": "Last Name", "class": "block w-full px-4 py-2 mt-1 border rounded-md"}),
		label=""
	)
    email = forms.EmailField(
		required=True,
		widget=forms.widgets.EmailInput(attrs={"placeholder": "Email Address", "class": "block w-full px-4 py-2 mt-1 border rounded-md"}),
		label=""
	)
    
# def profile_edit(request):
#     if request.method == 'POST':
#         if 'profile_form' in request.POST:
#             profile_form = ProfileForm(request.POST, instance=request.user)
#             if profile_form.is_valid():
#                 profile_form.save()
#                 # Redirect or indicate success
#         elif 'password_form' in request.POST:
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 password_form.save()
#                 # Redirect or indicate success
#         elif 'photo_form' in request.POST:
#             photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
#             if photo_form.is_valid():
#                 photo_form.save()
#                 # Redirect or indicate success
#     else:
#         profile_form = ProfileForm(instance=request.user)
#         password_form = PasswordChangeForm(request.user)
#         photo_form = ProfilePhotoForm(instance=request.user.profile)

#     return render(request, 'profile_edit.html', {
#         'profile_form': profile_form,
#         'password_form': password_form,
#         'photo_form': photo_form
#     })

    class Meta:
        model = Record
        exclude = ("user",)
