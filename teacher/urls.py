from django.urls import path
from .views import (
    create_subject, teacher_subjects, subject_lessons, create_lesson,
    download_lesson_file,lesson_detail, view_lesson_file , create_assignment,
    create_quiz, subject_quizzes, quiz_detail, edit_quiz
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create-subject/', create_subject, name='create_subject'),
    path('teacher/subjects/', teacher_subjects, name='teacher_subjects'),
    path('lesson/create/<int:subject_id>/', create_lesson, name='create_lesson'),
    path('subject/<int:subject_id>/lessons/', subject_lessons, name='subject_lessons'),
    path('lesson/download/<int:lesson_id>/', download_lesson_file, name='download_lesson_file'),
    path('lesson/<int:lesson_id>/', lesson_detail, name='lesson_detail'),
    path('lesson/view/<int:lesson_id>/', view_lesson_file, name='view_lesson_file'),
    path('subject/<int:subject_id>/create-quiz/', create_quiz, name='create_quiz'),
    path('subject/<int:subject_id>/quizzes/', subject_quizzes, name='subject_quizzes'),
    path('quiz/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/edit/', edit_quiz, name='edit_quiz'),
    path('subject/<int:subject_id>/create-assignments/', create_assignment, name='create_quiz'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
