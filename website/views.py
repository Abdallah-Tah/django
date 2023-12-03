from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse

from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


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
        return render(request, 'home.html', {'records': records})


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
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            user = authenticate(username=username, password=form.cleaned_data['password1'])
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('dashboard')
        else:
            # Directly render the page with the form containing errors
            messages.error(request, "There was an error with your registration. Please try again.")
            return render(request, 'home/register.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'home/register.html', {'form': form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
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
        return render(request, 'add_record.html', {'form': form})
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
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('home')


def profile_edit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated...")
                return redirect('dashboard')
        else:
            form = SignUpForm(instance=request.user)

        # Make sure the template path includes the 'auth' directory.
        return render(request, 'auth/profile_edit.html', {'form': form})

    else:
        messages.error(request,
                       "You Must Be Logged In...")  # This should probably be an error message instead of a success message.
        return redirect('login')


def pick_course(request):

    return render(request, 'course/profile_pick_course.html')
    #return HttpResponse("Your response content")
    #return redirect('pick_course')
