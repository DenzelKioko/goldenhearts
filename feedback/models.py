from django.db import models
from accounts.models import User
from programs.models import Program

# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="feedback", null=True, blank=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)  # scale of 1–10
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} ({self.rating}/10)"