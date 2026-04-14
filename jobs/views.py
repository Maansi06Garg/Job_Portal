from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job
from .forms import JobForm
from applications.models import Application


# Create Job (Employer only)

@login_required
def create_job(request):

    if request.user.user_type != 'employer':
        return redirect('home')

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.employer = request.user

            job.save()

            return redirect('job_list')

    else:
        form = JobForm()

    return render(
        request,
        'jobs/create_job.html',
        {'form': form}
    )


# Job List

def job_list(request):

    jobs = Job.objects.all().order_by('-created_at')

    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    salary = request.GET.get('salary')
    experience = request.GET.get('experience')

    # Keyword Search
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Location Filter
    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    # Salary Filter
    if salary:
        jobs = jobs.filter(
            salary__gte=salary
        )

    # Experience Filter
    if experience:
        jobs = jobs.filter(
            experience_required__lte=experience
        )

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs
        }
    )

# Job Detail

def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id
    )

    has_applied = False

    if request.user.is_authenticated:

        if request.user.user_type == 'jobseeker':

            has_applied = Application.objects.filter(
                job=job,
                applicant=request.user
            ).exists()

    return render(
        request,
        'jobs/job_detail.html',
        {
            'job': job,
            'has_applied': has_applied
        }
    )