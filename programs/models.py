from django.db import models
from accounts.models import User

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="programs_created")

    def __str__(self):
        return self.name
