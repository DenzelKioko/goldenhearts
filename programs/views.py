# programs/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from django.utils import timezone
from .models import Program

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'
    ordering = ['date_created']
    
    def get_queryset(self):
        return Program.objects.filter(is_active=True).annotate(
            event_count=Count('events'),
            upcoming_event_count=Count('events', filter=Q(events__date__gte=timezone.now().date()))
        )

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = self.object.events.order_by('-date', '-time')[:5]  # Latest 5 events
        context['upcoming_events'] = self.object.events.filter(
            date__gte=timezone.now().date()
        ).order_by('date', 'time')[:3]  # Next 3 upcoming events
        return context
