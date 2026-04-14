from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import (
    JobSeekerSignUpForm,
    EmployerSignUpForm
)


def home(request):
    return render(request, 'accounts/home.html')


# Job Seeker Signup

def jobseeker_signup(request):

    if request.method == 'POST':
        form = JobSeekerSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = JobSeekerSignUpForm()

    return render(
        request,
        'accounts/jobseeker_signup.html',
        {'form': form}
    )


# Employer Signup

def employer_signup(request):

    if request.method == 'POST':
        form = EmployerSignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    else:
        form = EmployerSignUpForm()

    return render(
        request,
        'accounts/employer_signup.html',
        {'form': form}
    )


# Login

def user_login(request):

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()
            login(request, user)

            next_page = request.POST.get('next') or request.GET.get('next')
            return redirect(next_page or 'job_list')

    else:
        form = AuthenticationForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )


# Logout

def user_logout(request):
    logout(request)
    return redirect('home')