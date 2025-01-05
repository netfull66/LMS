import os
from django.shortcuts import render, redirect ,get_object_or_404
from .forms import SubjectForm , LessonForm, QuizForm, QuestionForm, AssignmentForm
from .models import Subject ,Lesson, Quiz, Question , Assignment
from django.http import HttpResponse, Http404
from django.contrib import messages
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


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'teacher/lesson_detail.html', {'lesson': lesson})

def view_lesson_file(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if not lesson.files:
        raise Http404("File not found.")
    
    file_path = lesson.files.path
    
    if not os.path.exists(file_path):
        raise Http404("File not found.")
    
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    
    # Set the content type based on file extension
    content_types = {
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain',
    }
    
    content_type = content_types.get(file_extension, 'application/octet-stream')
    
    # Read and return the file
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=content_type)
        # Allow iframe embedding and same-origin requests
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['Content-Security-Policy'] = "default-src 'self'; frame-ancestors 'self'"
        return response


def create_quiz(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        
        if quiz_form.is_valid():
            # Create quiz instance
            quiz = quiz_form.save(commit=False)
            quiz.subject = subject  # Associate the quiz with the subject
            quiz.save()  # Save the quiz to the database

            # Handle questions
            for i in range(1, int(request.POST.get('question_count', 1)) + 1):
                question_text = request.POST.get(f'question{i}')
                question_type = request.POST.get(f'questionType{i}')
                answer = request.POST.get(f'answer{i}')
                
                if question_text and question_type and answer:
                    # Create question instance
                    question = Question(
                        quiz=quiz,
                        question_text=question_text,
                        question_type=question_type,
                        correct_answer=answer,
                        points=1  # Default value, you can make this configurable
                    )
                    
                    # Save choices for multiple choice questions
                    if question_type == 'multiple_choice':
                        for j in range(1, 5):
                            choice = request.POST.get(f'choice{i}_{j}')
                            if choice:
                                setattr(question, f'choice_{j}', choice)
                    
                    # Save the question with all its data
                    question.save()
            
            messages.success(request, "Quiz created successfully!")
            return redirect('subject_quizzes', subject_id=subject.id)  # Redirect to the quizzes page
            
        else:
            print("Form errors:", quiz_form.errors)  # Debug print
    else:
        quiz_form = QuizForm()

    return render(request, 'teacher/create_quiz.html', {
        'quiz_form': quiz_form,
        'subject': subject
    })

def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            # Redirect to the same page to add more questions or to a summary page
            return redirect('add_questions', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()

    return render(request, 'teacher/add_questions.html', {'form': question_form, 'quiz': quiz})

def subject_quizzes(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    # Ensure the user is a teacher and is the teacher of the subject
    if request.user.role != 'teacher' or subject.teacher != request.user:
        return HttpResponse("You do not have permission to view these quizzes.", status=403)

    quizzes = subject.quizzes.all()
    return render(request, 'teacher/subject_quizzes.html', {'subject': subject, 'quizzes': quizzes})

def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            messages.success(request, "Quiz updated successfully!")
            return redirect('quiz_detail', quiz_id=quiz.id)
    else:
        form = QuizForm(instance=quiz)

    return render(request, 'teacher/edit_quiz.html', {'form': form, 'quiz': quiz})

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()  # Assuming 'questions' is the related name for questions in the Quiz model
    return render(request, 'teacher/quiz_detail.html', {'quiz': quiz, 'questions': questions})

@login_required
def create_assignment(request, subject_id):
    if not request.user.is_authenticated:
        return redirect('login')
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.subject = subject
            assignment.teacher = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    
    return render(request, 'teacher/create_assignment.html', {
        'form': form,
        'subject': subject
    })