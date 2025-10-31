# programs/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.utils import timezone
from .models import Program
from .forms import ProgramForm

# Helper class
class AdminChecker:
    @staticmethod
    def is_admin(user):
        return user.is_authenticated and user.role == 'admin'

# Public Views
class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        return Program.objects.filter(is_active=True).annotate(
            event_count=Count('events'),
            upcoming_event_count=Count('events', filter=Q(events__date__gte=timezone.now().date()))
        ).order_by('-date_created')


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

# Admin-Only Views
class ProgramCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'programs/program_form.html'
    success_url = reverse_lazy('programs:program_list')
    
    def test_func(self):
        return AdminChecker.is_admin(self.request.user)
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, f'Program "{form.instance.name}" created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Program'
        return context

class ProgramUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'programs/program_form.html'
    
    def test_func(self):
        return AdminChecker.is_admin(self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('programs:program_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f'Program "{form.instance.name}" updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit {self.object.name}'
        return context

class ProgramDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Program
    template_name = 'programs/program_confirm_delete.html'
    success_url = reverse_lazy('programs:program_list')
    
    def test_func(self):
        return AdminChecker.is_admin(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        program = self.get_object()
        messages.success(request, f'Program "{program.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    