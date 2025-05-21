from django import forms
from .models import Project, Meeting, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'manager', 'members', 'budget']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'members': forms.SelectMultiple(attrs={'class': 'select2'}),
        }

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'location', 'duration', 'notes', 'project', 'participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'participants': forms.SelectMultiple(attrs={'class': 'select2'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'project', 'meeting', 'due_date', 'status', 'priority']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'due_date': forms.TextInput(attrs={
                'class': 'form-control jalali-date-datepicker',
                'autocomplete': 'off',
                'id': 'due_date'  # Added ID for easier selection
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'meeting': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

