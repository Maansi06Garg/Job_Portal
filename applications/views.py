from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.models import JobSeekerProfile

from .models import Application
from .forms import ApplicationForm
from jobs.models import Job


@login_required
def apply_job(request, job_id):

    if request.user.user_type != 'jobseeker':
        return redirect('home')

    job = get_object_or_404(
        Job,
        id=job_id
    )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(commit=False)

            application.job = job

            application.applicant = request.user

            application.save()

            return redirect('job_list')

    else:
        form = ApplicationForm()

    return render(
        request,
        'applications/apply_job.html',
        {
            'form': form,
            'job': job
        }
    )

@login_required
def view_applicants(request, job_id):

    if request.user.user_type != 'employer':
        return redirect('home')

    job = Job.objects.get(
        id=job_id,
        employer=request.user
    )

    applications = Application.objects.filter(
        job=job
    )

    return render(
        request,
        'applications/view_applicants.html',
        {
            'job': job,
            'applications': applications
        }
    )

@login_required
def update_application_status(
    request,
    application_id
):

    if request.user.user_type != 'employer':
        return redirect('home')

    application = Application.objects.get(
        id=application_id
    )

    status = request.POST.get('status')

    application.status = status
    application.save()

    return redirect(
        'view_applicants',
        job_id=application.job.id
    )

@login_required
def my_applications(request):

    if request.user.user_type != 'jobseeker':
        return redirect('home')

    applications = Application.objects.filter(
        applicant=request.user
    ).order_by('-applied_at')

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications
        }
    )