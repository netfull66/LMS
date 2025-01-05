from django.db import models
from welcome.models import User
from django.utils import timezone
from datetime import datetime

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

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=200)
    files = models.FileField(upload_to='lesson_files/', null=True, blank=True)
    video_link = models.URLField(max_length=200, null=True, blank=True)

    def get_youtube_embed_url(self):
        """Convert YouTube URL to embed URL if it's a YouTube video"""
        video_link = self.video_link
        if not video_link:
            return None
            
        if 'youtube.com/embed/' in video_link:
            return video_link
            
        if 'youtube.com/watch?v=' in video_link:
            return video_link.replace('watch?v=', 'embed/')
            
        if 'youtu.be/' in video_link:
            video_id = video_link.split('/')[-1]
            return f'https://www.youtube.com/embed/{video_id}'
            
        return video_link

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='quizzes')
    description = models.TextField(blank=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quizzes"

    def str(self):
        return self.title

    @property
    def is_active(self):
        now = timezone.now()
        start = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
        end = timezone.make_aware(datetime.combine(self.end_date, self.end_time))
        return start <= now <= end

class Question(models.Model):
    QUESTION_TYPES = (
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    correct_answer = models.TextField()
    points = models.PositiveIntegerField(default=1)
    choice_1 = models.CharField(max_length=200, blank=True, null=True)
    choice_2 = models.CharField(max_length=200, blank=True, null=True)
    choice_3 = models.CharField(max_length=200, blank=True, null=True)
    choice_4 = models.CharField(max_length=200, blank=True, null=True)
    
    def str(self):
        return f"{self.quiz.title} - {self.question_text[:50]}"


class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-due_date']
        verbose_name_plural = "Assignments"

    def _str_(self):
        return f"{self.subject.name} - {self.title}"

    @property
    def is_overdue(self):
        return timezone.now() > self.due_date