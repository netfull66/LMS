from django import forms
from .models import School

class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'excel_file']