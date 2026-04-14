from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

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