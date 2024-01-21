from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import generic
from django.db import transaction
from django.urls import reverse
from django.contrib import messages
from quizapp.models import Quiz, Question, AnswerOption, UserAnswer

# Create your views here.
class QuizListView(generic.ListView):
    """
    View for listing all active quizzes.
    """
    model = Quiz
    template_name = "quiz_list.html"
    context_object_name = "quiz_list"

    def get_queryset(self):
        """
        Return only active quizzes.
        """
        return Quiz.objects.filter(pub_date__lte=timezone.now())

class QuizDetailView(generic.DetailView):
    """
    View for displaying a specific quiz and its questions.
    """
    model = Quiz
    template_name = "quiz_detail.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.filter(quiz=self.object)
        return context

def submit_quiz(request, quiz_id):
    if request.method == 'POST':
        quiz = Quiz.objects.get(pk=quiz_id)
        questions = Question.objects.filter(quiz=quiz)
        user_answers = []

        try:
            with transaction.atomic():
                for question in questions:
                    answer_option_id = request.POST.get(f'question_{question.id}')
                    selected_answer = AnswerOption.objects.get(pk=answer_option_id) if answer_option_id else None

                    # Check if the selected answer is correct
                    is_correct = selected_answer.is_correct if selected_answer else False

                    # Save the user's answer
                    user_answer = UserAnswer.objects.create(
                        question=question,
                        selected_answer=selected_answer,
                    )
                    user_answers.append({'user_answer': user_answer, 'is_correct': is_correct})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect(reverse('quiz:detail', args=[quiz.id]))

        context = {
            'quiz': quiz,
            'user_answers': user_answers,
        }

        return render(request, 'quiz_results.html', context)

    else:
        # Redirect to the quiz detail page if not a POST request
        return redirect(reverse('quiz:detail', args=[quiz_id]))

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def student(request):
    return render(request, 'student.html')

def teacher(request):
    return render(request, 'teacher.html')

def contact(request):
    return render(request, 'contact.html')