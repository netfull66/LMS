from django.shortcuts import render
import pandas as pd
from django.shortcuts import render, redirect
from .forms import SchoolRegistrationForm
from django.contrib.auth.hashers import make_password
from .models import School, User
from django.core.exceptions import ValidationError


def register(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the school instance but don't commit yet
            school = form.save(commit=False)

            # Process the uploaded file
            uploaded_file = request.FILES['excel_file']
            try:
                # Detect file format and load data
                if uploaded_file.name.endswith('.xlsx') or uploaded_file.name.endswith('.xls'):
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                elif uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    raise ValidationError("Invalid file format. Please upload an Excel or CSV file.")

                # Validate required columns
                required_columns = {'role', 'email', 'name'}
                if not required_columns.issubset(df.columns):
                    raise ValidationError(f"The file must contain the following columns: {', '.join(required_columns)}")

                # Clean and process data
                df['role'] = df['role'].str.strip().str.lower()
                df['email'] = df['email'].str.strip()
                df['name'] = df['name'].str.strip()

                # Count roles for the school
                school.student_numbers = len(df[df['role'] == 'student'])
                school.teacher_numbers = len(df[df['role'] == 'teacher'])
                school.school_admin_numbers = len(df[df['role'] == 'school_admin'])

                # Save the school instance
                school.save()

                # Register users
                for _, row in df.iterrows():
                    try:
                        # Create a username if not provided
                        username = row['email'].split('@')[0]

                        # Ensure unique username
                        if User.objects.filter(username=username).exists():
                            username = f"{username}_{User.objects.count() + 1}"

                        # Create and save the user
                        user = User(
                            username=username,
                            name=row['name'],
                            email=row['email'],
                            role=row['role'],
                            gender=row.get('gender', '').strip()[:1].upper() if 'gender' in row else None,
                            religion=row.get('religion', '').strip().capitalize() if 'religion' in row else None,
                            grade=row.get('grade', None),
                            class_name=row.get('class_name', None),
                            password=make_password('defaultpassword'),  # Default password
                        )
                        user.save()
                    except Exception as e:
                        print(f"Error saving user: {e}")
                        continue  # Skip problematic rows

            except ValidationError as ve:
                print(f"Validation error: {ve}")
            except pd.errors.EmptyDataError:
                print("The uploaded file is empty.")
            except Exception as e:
                print(f"Unexpected error: {e}")

    else:
        form = SchoolRegistrationForm()
    return render(request, 'register.html', {'form': form})
