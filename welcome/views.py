from django.shortcuts import render
import pandas as pd
from django.shortcuts import render, redirect
from .forms import SchoolRegistrationForm
from .models import School, User

def register(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the school instance but don't commit yet
            school = form.save(commit=False)

            # Process the Excel file
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            # Check if the 'role' column exists and clean data
            if 'role' in df.columns:
                df['role'] = df['role'].str.strip().str.lower()  # Clean role data
                school.student_numbers = len(df[df['role'] == 'student'])
                school.teacher_numbers = len(df[df['role'] == 'teacher'])
                school.school_admin_numbers = len(df[df['role'] == 'school_admin'])
            else:
                # Handle missing role column
                school.student_numbers = 0
                school.teacher_numbers = 0
                school.school_admin_numbers = 0

            # Save the school with calculated values
            school.save()

    else:
        form = SchoolRegistrationForm()
    return render(request, 'register.html', {'form': form})