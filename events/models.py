from django.db import models
from accounts.models import User
from programs.models import Program

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="events", null=True, blank=True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="organized_events")

    def __str__(self):
        return self.title