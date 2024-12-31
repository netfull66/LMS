from django.urls import path
from .views import create_subject,teacher_subjects,subject_lessons,create_lesson,download_lesson_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-subject/', create_subject, name='create_subject'),
    path('teacher/subjects/', teacher_subjects, name='teacher_subjects'),
    path('lesson/create/<int:subject_id>/', create_lesson, name='create_lesson'),
    path('subject/<int:subject_id>/lessons/', subject_lessons, name='subject_lessons'),
    path('lesson/download/<int:lesson_id>/', download_lesson_file, name='download_lesson_file'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
