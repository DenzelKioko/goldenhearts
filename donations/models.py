from django.db import models
from accounts.models import User
from programs.models import Program

# Create your models here.
class Donation(models.Model):
    DONATION_TYPE = (
        ('money', 'Money'),
        ('items', 'Items'),
        ('service', 'Service'),
    )
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="donations", null=True, blank=True)
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.username} - {self.donation_type}"