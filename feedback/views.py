from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class FeedbackView(TemplateView):
    """Placeholder view for the feedback submission form."""
    # This will be converted to a FormView later
    template_name = 'feedback/submit_feedback.html'
