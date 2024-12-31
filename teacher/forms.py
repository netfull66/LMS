from django import forms
from welcome.models import User
from .models import Subject ,Lesson

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