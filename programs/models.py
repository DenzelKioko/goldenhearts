from django.db import models
from accounts.models import User
from django.utils import timezone


class Program(models.Model):
    CATEGORY_CHOICES = (
        ('health', 'Health'),
        ('education', 'Education'),
        ('environment', 'Environment'),
        ('community', 'Community Support'),
        
    )

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='community')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        limit_choices_to={'role': 'admin'}, related_name='created_programs'
    )
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_created']
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
