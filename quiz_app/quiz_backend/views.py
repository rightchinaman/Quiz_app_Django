# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from .models import Question, QuizSession
import random

def start_quiz(request):
    session = QuizSession.objects.create()
    request.session['quiz_session_id'] = session.id
    return redirect('get_question')

def get_question(request):
    session_id = request.session.get('quiz_session_id')
    if not session_id:
        return redirect('start_quiz')

    session = QuizSession.objects.get(id=session_id)

    # Get remaining questions
    remaining_questions = session.remaining_questions()

    if not remaining_questions:
        return redirect('quiz_summary')  # All questions have been asked, go to summary

    # Pick a random question from remaining questions
    question = random.choice(remaining_questions)
    
    # Mark this question as asked in the session
    session.questions_asked.add(question)
    session.save()

    time_left = session.time_left()  # Get the remaining time for the session

    return render(request, 'quiz/question.html', {'question': question, 'time_left': time_left})

def submit_answer(request):
    if request.method == 'POST':
        session_id = request.session.get('quiz_session_id')
        if not session_id:
            return JsonResponse({'error': 'No active quiz session'}, status=400)

        session = QuizSession.objects.get(id=session_id)
        
        # Check if time is up
        if session.is_time_up():
            return redirect('quiz_summary')

        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('selected_option')
        
        question = Question.objects.get(id=question_id)
        session.total_questions += 1

        if question.correct_option == selected_option:
            session.correct_answers += 1
        else:
            session.incorrect_answers += 1

        # Increment the current question index
        session.current_question_index += 1
        session.save()

        # Check if it's the last question and redirect to the summary page if so
        if session.current_question_index >= len(Question.objects.all()):
            return redirect('quiz_summary')

        return redirect('get_question')  # Show the next question

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def quiz_summary(request):
    session_id = request.session.get('quiz_session_id')
    if not session_id:
        return redirect('start_quiz')

    session = QuizSession.objects.get(id=session_id)
    return render(request, 'quiz/summary.html', {
        'total_questions': session.total_questions,
        'correct_answers': session.correct_answers,
        'incorrect_answers': session.incorrect_answers
    })


