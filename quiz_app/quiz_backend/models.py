# models.py
from django.db import models
from datetime import timedelta
from django.utils import timezone

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

class QuizSession(models.Model):
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    current_question_index = models.IntegerField(default=0)
    questions_asked = models.ManyToManyField(Question, blank=True)  # Track the current question index
    start_time = models.DateTimeField(default=timezone.now)  # Time when the quiz started
    time_limit = models.IntegerField(default=300)  # Time limit in seconds (e.g., 5 minutes)

    def remaining_questions(self):
        """Return questions not yet asked in this session."""
        return Question.objects.exclude(id__in=self.questions_asked.values_list('id', flat=True))
    
    def time_left(self):
        """Return the remaining time in seconds"""
        elapsed_time = (timezone.now() - self.start_time).total_seconds()
        return max(self.time_limit - int(elapsed_time), 0)  # Prevent negative time

    def is_time_up(self):
        """Check if the time is up"""
        return self.time_left() <= 0
