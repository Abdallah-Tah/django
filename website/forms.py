from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'block w-full px-4 py-2 mt-1 border rounded-md', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'block w-full px-4 py-2 mt-1 border rounded-md'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        # Include Tailwind classes for the help text if needed

        self.fields['password1'].widget.attrs['class'] = 'block w-full px-4 py-2 mt-1 border rounded-md'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        # Include Tailwind classes for the help text if needed

        self.fields['password2'].widget.attrs['class'] = 'block w-full px-4 py-2 mt-1 border rounded-md'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        # Include Tailwind classes for the help text if needed


# Create Add Record Form
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
    # if request.method == 'POST':
    #     if 'profile_form' in request.POST:
    #         profile_form = ProfileForm(request.POST, instance=request.user)
    #         if profile_form.is_valid():
    #             profile_form.save()
    #             # Redirect or indicate success
    #     elif 'password_form' in request.POST:
    #         password_form = PasswordChangeForm(request.user, request.POST)
    #         if password_form.is_valid():
    #             password_form.save()
    #             # Redirect or indicate success
    #     elif 'photo_form' in request.POST:
    #         photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=request.user.profile)
    #         if photo_form.is_valid():
    #             photo_form.save()
    #             # Redirect or indicate success
    # else:
    #     profile_form = ProfileForm(instance=request.user)
    #     password_form = PasswordChangeForm(request.user)
    #     photo_form = ProfilePhotoForm(instance=request.user.profile)

    # return render(request, 'profile_edit.html', {
    #     'profile_form': profile_form,
    #     'password_form': password_form,
    #     'photo_form': photo_form
    # })

    class Meta:
        model = Record
        exclude = ("user",)