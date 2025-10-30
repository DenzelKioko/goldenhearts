from django import forms
from .models import Event, Registration
from programs.models import Program

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'program', 'description', 'date', 'time', 'location', 'capacity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }
        labels = {
            'capacity': 'Maximum Capacity (0 for unlimited)',
            'program': 'Associated Program'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.filter(is_active=True)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['notes']

class RegistrationApprovalForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['approved', 'notes']