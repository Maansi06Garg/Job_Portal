from django.urls import path
from . import views

urlpatterns = [

    path(
        'create/',
        views.create_job,
        name='create_job'
    ),

    path(
        '',
        views.job_list,
        name='job_list'
    ),

    path(
        '<int:job_id>/',
        views.job_detail,
        name='job_detail'
    ),

]