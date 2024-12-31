from django.shortcuts import render, redirect
from .forms import SubjectForm
from .models import Subject
from django.contrib.auth.decorators import login_required

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