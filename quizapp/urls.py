from django.urls import path
from quizapp import views

app_name = "quiz"

urlpatterns = [
    path("allquiz", views.QuizListView.as_view(), name="list"),
    path("<int:pk>", views.QuizDetailView.as_view(), name="detail"),
    path("<int:quiz_id>/submit", views.submit_quiz, name="submit"),
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("about", views.about, name="about"),
    path("student", views.student, name="student"),
    path("teacher", views.teacher, name="teacher"),
    path("contact", views.contact, name="contact"),
]
