#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goldenhearts.settings')
django.setup()

from programs.models import Program
from accounts.models import User
from django.db.models import Count, Q
from django.utils import timezone

print("=== PROGRAM TEST ===")
programs = Program.objects.filter(is_active=True).annotate(
    event_count=Count('events'),
    upcoming_event_count=Count('events', filter=Q(events__date__gte=timezone.now().date()))
).order_by('-date_created')

print(f"Found {programs.count()} programs:")
for p in programs:
    print(f"- {p.name} ({p.get_category_display()}) - Events: {p.event_count}")

print("\n=== USER TEST ===")
users = User.objects.all()
for u in users:
    print(f"- {u.email} (role: {u.role})")