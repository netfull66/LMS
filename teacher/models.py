from django.db import models
from welcome.models import User

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