from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobSeekerProfile, EmployerProfile


class JobSeekerSignUpForm(UserCreationForm):

    skills = forms.CharField(widget=forms.Textarea)
    experience = forms.IntegerField()
    location = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'jobseeker'

        if commit:
            user.save()

            JobSeekerProfile.objects.create(
                user=user,
                skills=self.cleaned_data['skills'],
                experience=self.cleaned_data['experience'],
                location=self.cleaned_data['location']
            )

        return user



class EmployerSignUpForm(UserCreationForm):

    company_name = forms.CharField(max_length=200)
    company_website = forms.URLField()
    company_description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'employer'

        if commit:
            user.save()

            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                company_website=self.cleaned_data['company_website'],
                company_description=self.cleaned_data['company_description']
            )

        return user