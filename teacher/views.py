import os
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import SubjectForm , LessonForm
from .models import Subject ,Lesson
from django.http import HttpResponse, Http404

def create_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')  # Redirect to a subject list page or other desired page
    else:
        form = SubjectForm()
    
    return render(request, 'teacher/create_subject.html', {'form': form})

def teacher_subjects(request):
    if not request.user.is_authenticated:
        # Redirect to login page if the user is not authenticated
        return redirect('login')  # Adjust 'login' to the correct name of your login route

    # Fetch the subjects for the teacher
    subjects = Subject.objects.filter(teacher=request.user)

    # Render the subjects for the teacher
    return render(request, 'teacher/teacher_subjects.html', {'subjects': subjects})

def subject_lessons(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    lessons = subject.lessons.all()  # Fetch all lessons related to the subject
    return render(request, 'teacher/subject_lessons.html', {'subject': subject, 'lessons': lessons})


def create_lesson(request, subject_id):
    # Fetch the subject object based on the subject_id
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, request.FILES)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.subject = subject  # Automatically assign the subject to the lesson
            lesson.save()  # Save the lesson

            # After saving, redirect to the subject's lessons page
            return redirect('subject_lessons', subject_id=subject.id)
    else:
        form = LessonForm()

    return render(request, 'teacher/create_lesson.html', {
        'form': form,
        'subject': subject  # Pass subject to the template for display
    })


def download_lesson_file(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if not lesson.files:
        raise Http404("File not found.")
    
    # Get the file path
    file_path = lesson.files.path

    # Debug: print the file path to verify
    print(f"File path: {file_path}")

    # Check if file exists
    if not os.path.exists(file_path):
        raise Http404("File not found.")
    
    # If the file exists, serve it
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{lesson.files.name}"'
        return response
