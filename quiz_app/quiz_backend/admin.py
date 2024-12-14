# Register your models here.
from django.contrib import admin
from .models import Question, QuizSession

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'correct_option')
    search_fields = ('text',)
    list_filter = ('correct_option',)

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('total_questions', 'correct_answers', 'incorrect_answers')
    list_filter = ('total_questions',)