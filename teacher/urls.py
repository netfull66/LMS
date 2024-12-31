from django.urls import path
from .views import create_subject,teacher_subjects

urlpatterns = [
    path('create-subject/', create_subject, name='create_subject'),
    path('teacher/subjects/', teacher_subjects, name='teacher_subjects'),

]
