from django import forms
from welcome.models import User
from .models import Subject ,Lesson
from django.forms import inlineformset_factory
from .models import Quiz, Question

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'grade', 'class_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter the teacher queryset to show only users with role 'teacher'
        self.fields['teacher'].queryset = User.objects.filter(role='teacher')

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['name', 'files', 'video_link']



class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'correct_answer', 'points',
                 'choice_1', 'choice_2', 'choice_3', 'choice_4']
        widgets = {
            'question_text': forms.Textarea(attrs={'rows': 3}),
            'correct_answer': forms.Textarea(attrs={'rows': 2}),
        }

# Create a formset for handling multiple questions at once
QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    form=QuestionForm,
    extra=3,  # Number of empty forms to display
    can_delete=True,
    min_num=1,  # Minimum number of forms
    validate_min=True,  # Enforce minimum number of forms
)