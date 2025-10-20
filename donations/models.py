from django.db import models
from accounts.models import User
# Ensure you have 'from programs.models import Program' if Program is defined there

class Donation(models.Model):
    # Choices for the type of donation
    DONATION_TYPE = (
        ('money', 'Money'),
        ('items', 'Items'),
        ('service', 'Service'),
    )
    
    # --- Required Changes for Flexibility and Accountability ---
    
    # 1. Donor field is now optional (allows guest/anonymous donations)
    donor = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="donations",
        null=True, blank=True,
        # Note: CASCADE changed to SET_NULL to preserve donation history if user deletes account
        limit_choices_to={'role__in': ['patron', 'admin']} 
    )
    
    # 2. Fields to capture info for non-logged-in donors
    guest_name = models.CharField(max_length=255, blank=True, null=True)
    guest_email = models.EmailField(blank=True, null=True)
    
    # 3. Accountability fields
    transaction_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # Status is crucial for tracking payment success/failure
    STATUS_CHOICES = (
        ('pending', 'Pending Payment'),
        ('success', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # --- Existing Fields ---
    program = models.ForeignKey(
        'programs.Program', on_delete=models.SET_NULL, related_name="donations",
        null=True, blank=True
    )
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ['-date']

    def __str__(self):
        # Display guest email if donor is None
        donor_identifier = self.donor.email if self.donor else self.guest_email or 'Anonymous'
        return f"{donor_identifier} - {self.get_donation_type_display()} ({self.date.date()})"
