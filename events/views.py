from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from .models import Event, Registration
from .forms import EventForm, RegistrationForm, RegistrationApprovalForm

# Helper functions
def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

def is_patron(user):
    return user.is_authenticated and user.role == 'patron'

# --- Public Views ---
def event_list(request):
    events = Event.objects.all().order_by('-date', '-time')
    
    # Filter by query parameters
    upcoming = request.GET.get('upcoming')
    if upcoming:
        events = events.filter(date__gte=timezone.now().date())
    
    return render(request, 'events/event_list.html', {
        'events': events,
        'upcoming_filter': bool(upcoming)
    })

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user_registration = None
    
    if request.user.is_authenticated:
        user_registration = Registration.objects.filter(
            event=event, 
            user=request.user
        ).first()

    # Handle registration
    if request.method == 'POST' and request.user.is_authenticated:
        if not user_registration:
            if event.is_full:
                messages.error(request, "This event is already full.")
            else:
                Registration.objects.create(event=event, user=request.user)
                messages.success(request, "Registration submitted! Awaiting approval.")
                return redirect('events:event_detail', event_id=event.id)
        else:
            messages.info(request, "You are already registered for this event.")

    return render(request, 'events/event_detail.html', {
        'event': event,
        'user_registration': user_registration,
    })

# --- Patron Views ---
@login_required
def my_registrations(request):
    if not is_patron(request.user):
        messages.error(request, "Access denied.")
        return redirect('events:event_list')
    
    registrations = Registration.objects.filter(user=request.user).select_related('event')
    
    return render(request, 'events/my_registrations.html', {
        'registrations': registrations
    })

@login_required
def cancel_registration(request, reg_id):
    registration = get_object_or_404(Registration, id=reg_id, user=request.user)
    event_id = registration.event.id
    
    if request.method == 'POST':
        registration.delete()
        messages.success(request, "Your registration has been cancelled.")
        return redirect('events:event_detail', event_id=event_id)
    
    return render(request, 'events/registration_confirm_cancel.html', {
        'registration': registration
    })

# --- Admin Views ---
@user_passes_test(is_admin)
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('events:event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_form.html', {
        'form': form, 
        'title': 'Create New Event'
    })

@user_passes_test(is_admin)
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_form.html', {
        'form': form, 
        'title': 'Edit Event'
    })

@user_passes_test(is_admin)
def manage_registrations(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registrations.select_related('user')
    
    return render(request, 'events/event_registrations.html', {
        'event': event,
        'registrations': registrations
    })

@user_passes_test(is_admin)
def approve_registration(request, reg_id):
    registration = get_object_or_404(Registration, id=reg_id)
    
    if request.method == 'POST':
        registration.approved = True
        registration.save()
        messages.success(request, f"Registration for {registration.user.email} approved.")
    
    return redirect('events:manage_registrations', event_id=registration.event.id)

@user_passes_test(is_admin)
def reject_registration(request, reg_id):
    registration = get_object_or_404(Registration, id=reg_id)
    event_id = registration.event.id
    
    if request.method == 'POST':
        registration.delete()
        messages.success(request, f"Registration for {registration.user.email} rejected.")
    
    return redirect('events:manage_registrations', event_id=event_id)

@user_passes_test(is_admin)
def check_in_registration(request, reg_id):
    registration = get_object_or_404(Registration, id=reg_id)
    
    if request.method == 'POST':
        if registration.approved:
            registration.is_checked_in = True
            registration.save()
            messages.success(request, f"{registration.user.email} checked in successfully.")
        else:
            messages.error(request, "Cannot check in unapproved registration.")
    
    return redirect('events:manage_registrations', event_id=registration.event.id)