from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'signup/jobseeker/',
        views.jobseeker_signup,
        name='jobseeker_signup'
    ),

    path(
        'signup/employer/',
        views.employer_signup,
        name='employer_signup'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
]