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
from django.db import connection, IntegrityError


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

    # Function to check if asanas for the week are completed
    def check_asanas_completed(week):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*)
                FROM to_do
                WHERE week_id = %s
                AND asana_id NOT IN (
                    SELECT asana_id 
                    FROM asanas_performed 
                    WHERE user_id = %s
                )""", [week, user.id])
            return cursor.fetchone()[0] == 0

    # select current week of progress
    with connection.cursor() as cursor:
        cursor.execute("""SELECT current_week from user_progress where user_id = %s""", [user.id])
        result = cursor.fetchone()

    if result is not None:
        week = result[0]


        # now select asanas for this week
        with connection.cursor() as cursor:
            cursor.execute("""SELECT asana_id from to_do where week_id = %s""", [week])
            result = cursor.fetchall()

        # for each asana retrieve steps from has_step relation
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT
                       a.id,
                       a.name,
                       JSON_OBJECTAGG(s.technique, subquery.image) AS steps
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
                           JSON_ARRAYAGG(i.image) AS image
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
            steps = cursor.fetchall()
            processed_steps = ()
            for step in steps:
                id = step[0]
                name = step[1]
                technique = json.loads(step[2])
                processed_steps = processed_steps + ((id, name, technique),)
        
        # with connection.cursor() as cursor:
        #     cursor.execute("SELECT MAX(week_id) FROM to_do")
        #     last_week = cursor.fetchone()[0]

        # Initialize or update current asana index
        if 'current_asana_index' not in request.session:
            request.session['current_asana_index'] = 0

        if request.GET.get('action') == 'next':
            current_asana_id = processed_steps[request.session['current_asana_index']][0]
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO asanas_performed (user_id, asana_id) 
                           SELECT %s, %s 
                           WHERE NOT EXISTS (
                               SELECT 1 FROM asanas_performed 
                               WHERE user_id = %s AND asana_id = %s
                           )""",
                        [user.id, current_asana_id, user.id, current_asana_id]
                    )
            except IntegrityError:
                # Handle the case where the insert operation fails (if needed)
                pass

            request.session['current_asana_index'] += 1

        elif request.GET.get('action') == 'previous':
            request.session['current_asana_index'] -= 1

        # is_last_step = week == last_week and request.session['current_asana_index'] == len(processed_steps) - 1

        # Ensure the index stays within bounds
        request.session['current_asana_index'] = max(0, min(request.session['current_asana_index'], len(processed_steps) - 1))

        # Select the current asana to display
        current_asana = processed_steps[request.session['current_asana_index']]

        return render(request, 'course/session.html', {'week': week, 'asana': current_asana})
    else:
        print("No result found for the given user_id.")
        return HttpResponse("Your response content")
