import json
from datetime import timezone

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .forms import SignUpForm, AddRecordForm
from .models import Record
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProgress
from django.db import connection
import datetime


def welcome(request):
    return render(request, 'home/index.html')


@login_required
def dashboard(request):
    # Assuming the user is logged in, request.user gives you the currently logged-in user
    current_user = request.user

    try:
        # Retrieve the UserProgress instance associated with the current user
        user_progress = UserProgress.objects.get(user=current_user)
    except UserProgress.DoesNotExist:
        # Handle the case where UserProgress entry does not exist for the current user
        user_progress_entry = None

    return render(request, 'auth/dashboard.html', {'user_progress': user_progress})


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
            user = form.save()  # Save the user and get the instance
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")

            with connection.cursor() as cursor:
                cursor.execute("""INSERT INTO user_progress
                VALUES(NULL,1,CURRENT_TIMESTAMP, 0, %s);""",
                               [user.id])

            connection.commit()

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


def session(request):
    # current user
    user = request.user
    # select current week of progress
    with connection.cursor() as cursor:
        cursor.execute("""SELECT current_week from user_progress where user_id = %s"""
                       , [user.id])

        # Fetch the result
        result = cursor.fetchone()
    # Check if the result is not None before accessing its value
    if result is not None:
        week = result[0]
        # now select asanas for this week
        with connection.cursor() as cursor:
            cursor.execute("""SELECT asana_id from to_do where week_id = %s"""
                           , [week])
            # Fetch the result
            result = cursor.fetchall()

        # for each asana retrieve steps from has_step relation
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                                a.id,
                                a.name,
                                JSON_OBJECTAGG(s.technique, subquery.image_urls) AS steps
                            FROM
                                to_do t
                            JOIN
                                has_steps hs ON t.asana_id = hs.asana_id
                            JOIN
                                step s ON hs.step_id = s.id
                            LEFT JOIN
                                asana a ON t.asana_id = a.id
                            LEFT JOIN (
                                SELECT
                                    s.id,
                                    JSON_ARRAYAGG(i.image_url) AS image_urls
                                FROM
                                    step s
                                LEFT JOIN
                                    image i ON s.id = i.step_id
                                GROUP BY
                                    s.id
                            ) subquery ON s.id = subquery.id
                            WHERE
                                t.week_id = %s
                            GROUP BY
                                a.id, a.name
                            ORDER BY
                                a.id;""", [week]
            )
            # Fetch the result
            steps = cursor.fetchall()
            processed_steps = ()
            for step in steps:
                id = step[0]
                name = step[1]
                technique = json.loads(step[2])
                processed_steps = processed_steps + ((id,name,technique),)

            print(processed_steps)

        return render(request, 'course/session.html', {'week': week, 'steps': processed_steps})
    else:
        print("No result found for the given user_id.")
        return HttpResponse("Your response content")

