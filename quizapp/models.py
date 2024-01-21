from django.db import models

# Create your models here.
class Quiz(models.Model):
    """
    Model representing a quiz with its text and description.
    """
    quiz_text = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.quiz_text

class Question(models.Model):
    """
    Model representing a question within a quiz with its text.
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    # order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question_text

class AnswerOption(models.Model):
    """
    Model representing an answer option for a question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

class UserAnswer(models.Model):
    """
    Model representing a user's answer to a question.
    """
    # user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(AnswerOption, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ("user", "question")
