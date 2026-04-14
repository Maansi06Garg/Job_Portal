from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ('jobseeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='jobseeker'
    )

class JobSeekerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    skills = models.TextField()

    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True
    )

    experience = models.IntegerField(default=0)

    location = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class EmployerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=200)

    company_website = models.URLField()

    company_description = models.TextField()

    def __str__(self):
        return self.company_name