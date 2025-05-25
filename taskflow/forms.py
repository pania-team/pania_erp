from django import forms
from .models import Project, Meeting, Task
from django_jalali.forms import jDateField
import jdatetime



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



# -------------------------------------------
class MeetingForm(forms.ModelForm):
    date = jDateField(
        widget=forms.TextInput(attrs={
            'data-jdp': 'true',
            'class': 'form-control',
            'placeholder': 'تاریخ جلسه',
            'autocomplete': 'off',
            'style': 'font-family: Vazirmatn; font-size: 11px'
        }),
        input_formats=['%Y-%m-%d'],  # Use hyphen format as required by jDateField
        label=''
    )

    def clean_date(self):
        date_value = self.cleaned_data.get('date')
        if date_value:
            # Convert any forward slashes to hyphens
            if isinstance(date_value, str):
                date_value = date_value.replace('/', '-')
                # Parse the date manually
                try:
                    year, month, day = map(int, date_value.split('-'))
                    return jdatetime.date(year, month, day)
                except (ValueError, TypeError):
                    raise forms.ValidationError('یک تاریخ معتبر وارد کنید.')
        return date_value

    class Meta:
        model = Meeting
        fields = ['title', 'date', 'location', 'duration', 'notes', 'project', 'participants']
        widgets = {
            'title': forms.TextInput(attrs={
                "placeholder": "عنوان جلسه",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'location': forms.TextInput(attrs={
                "placeholder": "محل برگزاری",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'duration': forms.NumberInput(attrs={
                "placeholder": "مدت زمان (دقیقه)",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                "placeholder": "یادداشت‌ها",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'project': forms.Select(attrs={
                'required': True,
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'participants': forms.SelectMultiple(attrs={
                'class': 'select2',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
        }
        labels = {
            'title': '',
            'date': '',
            'location': '',
            'duration': '',
            'notes': '',
            'project': '',
            'participants': '',
        }


# ------------------------------------------------

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

