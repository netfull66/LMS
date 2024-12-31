from django.contrib import admin
from .models import Subject ,Lesson

class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'video_link']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Subject)
