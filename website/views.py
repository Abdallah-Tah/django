from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProgress
import datetime
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def welcome(request):
    return render(request, 'home/index.html')  

@login_required
def dashboard(request):
    return render(request, 'auth/dashboard.html')

def login_user(request):
	return render(request, 'home/login.html')

def login_endpoint(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Authenticate using email instead of username
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=request.POST.get('password'))
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials.")
            return render(request, 'home/login.html', {'error_message': 'Invalid credentials.'})
    return render(request, 'home/login.html')

def home(request):
	records = Record.objects.all()
	# Check to see if logging in
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
		return render(request, 'home.html', {'records':records})



def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('login')

def about(request):
    return render(request, 'home/about.html')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the instance
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")

            user_progress = UserProgress(user_id=user.id, current_week=1, start_date=datetime.date.today())
            user_progress.save()

            return redirect('dashboard')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
            return render(request, 'home/register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'home/register.html', {'form': form})



def customer_record(request, pk):
	if request.user.is_authenticated:
		# Look Up Records
		customer_record = Record.objects.get(id=pk)
		return render(request, 'record.html', {'customer_record':customer_record})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')



def delete_record(request, pk):
	if request.user.is_authenticated:
		delete_it = Record.objects.get(id=pk)
		delete_it.delete()
		messages.success(request, "Record Deleted Successfully...")
		return redirect('home')
	else:
		messages.success(request, "You Must Be Logged In To Do That...")
		return redirect('home')


def add_record(request):
	form = AddRecordForm(request.POST or None)
	if request.user.is_authenticated:
		if request.method == "POST":
			if form.is_valid():
				add_record = form.save()
				messages.success(request, "Record Added...")
				return redirect('home')
		return render(request, 'add_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')


def update_record(request, pk):
	if request.user.is_authenticated:
		current_record = Record.objects.get(id=pk)
		form = AddRecordForm(request.POST or None, instance=current_record)
		if form.is_valid():
			form.save()
			messages.success(request, "Record Has Been Updated!")
			return redirect('home')
		return render(request, 'update_record.html', {'form':form})
	else:
		messages.success(request, "You Must Be Logged In...")
		return redirect('home')
	
@login_required
def profile_edit(request):
    if request.method == 'POST':
        if 'profile_form' in request.POST:
            profile_form = UserProfileForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('dashboard')

        elif 'password_form' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important to keep the user logged in after password change
                messages.success(request, "Password changed successfully.")
                return redirect('dashboard')

    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'auth/profile_edit.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })