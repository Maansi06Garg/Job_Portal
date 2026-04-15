from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

from .forms import (
    JobSeekerSignUpForm,
    EmployerSignUpForm
)

from django.contrib.auth.decorators import login_required
from jobs.models import Job
from applications.models import Application

@login_required
def dashboard(request):

    user = request.user

    # Employer Dashboard
    if user.user_type == 'employer':

        jobs = Job.objects.filter(employer=user)

        total_jobs = jobs.count()

        total_applications = Application.objects.filter(
            job__employer=user
        ).count()

        pending_applications = Application.objects.filter(
            job__employer=user,
            status='applied'
        ).count()

        shortlisted = Application.objects.filter(
            job__employer=user,
            status='shortlisted'
        ).count()

        accepted = Application.objects.filter(
            job__employer=user,
            status='accepted'
        ).count()

        rejected = Application.objects.filter(
            job__employer=user,
            status='rejected'
        ).count()

        context = {
            'total_jobs': total_jobs,
            'total_applications': total_applications,
            'pending_applications': pending_applications,
            'shortlisted': shortlisted,
            'accepted': accepted,
            'rejected': rejected,
        }

        return render(
            request,
            'accounts/employer_dashboard.html',
            context
        )

    # Job Seeker Dashboard
    elif user.user_type == 'jobseeker':

        total_applications = Application.objects.filter(
            applicant=user
        ).count()

        applied = Application.objects.filter(
            applicant=user,
            status='applied'
        ).count()

        shortlisted = Application.objects.filter(
            applicant=user,
            status='shortlisted'
        ).count()

        accepted = Application.objects.filter(
            applicant=user,
            status='accepted'
        ).count()

        rejected = Application.objects.filter(
            applicant=user,
            status='rejected'
        ).count()

        context = {
            'total_applications': total_applications,
            'applied': applied,
            'shortlisted': shortlisted,
            'accepted': accepted,
            'rejected': rejected,
        }

        return render(
            request,
            'accounts/jobseeker_dashboard.html',
            context
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
            return redirect(next_page or 'dashboard')

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