from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    RELIGION_CHOICES = [
        ('Christianity', 'Christianity'),
        ('Islam', 'Islam'),
    ]

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
        ('parent', 'Parent'),
        ('school_admin','School_admin')
    ]
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # Custom related name
        blank=True,
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    religion = models.CharField(max_length=20, choices=RELIGION_CHOICES)
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    grade = models.CharField(max_length=50, blank=True, null=True)
    class_name = models.CharField(max_length=50, blank=True, null=True)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teacher'
    )
    grade = models.CharField(max_length=50)
    class_name = models.CharField(max_length=50)

class School(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    student_numbers = models.PositiveIntegerField(blank=True, null=True)
    teacher_numbers = models.PositiveIntegerField(blank=True, null=True)
    school_admin_numbers = models.PositiveIntegerField(blank=True, null=True)
    excel_file = models.FileField(upload_to='school_files/')
