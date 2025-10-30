from django.db import models
from django.conf import settings
from django.utils import timezone
from programs.models import Program

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name='events'
    )
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_events'
    )
    
    class Meta:
        ordering = ['-date', '-time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_past(self):
        """Check if event date is in the past"""
        return self.date < timezone.now().date()
    
    @property
    def registered_count(self):
        return self.registrations.count()
    
    @property
    def approved_registrations_count(self):
        return self.registrations.filter(approved=True).count()
    
    @property
    def available_spots(self):
        return max(0, self.capacity - self.approved_registrations_count)
    
    @property
    def is_full(self):
        return self.capacity > 0 and self.approved_registrations_count >= self.capacity


class Registration(models.Model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='registrations'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='event_registrations'
    )
    approved = models.BooleanField(default=False)
    is_checked_in = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.user.email} - {self.event.title}"
    
    @property
    def can_check_in(self):
        """User can check in if approved and event is today or in the future"""
        return self.approved and not self.event.is_past