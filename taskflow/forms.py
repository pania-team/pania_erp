from django import forms
from .models import Project, Meeting, Task
from django_jalali.forms import jDateField
import jdatetime



class ProjectForm(forms.ModelForm):
    start_date = jDateField(
        widget=forms.TextInput(attrs={
            'data-jdp': 'true',
            'class': 'form-control',
            'placeholder': 'تاریخ شروع',
            'autocomplete': 'off',
            'style': 'font-family: Vazirmatn; font-size: 11px'
        }),
        input_formats=['%Y-%m-%d'],
        label=''
    )

    end_date = jDateField(
        widget=forms.TextInput(attrs={
            'data-jdp': 'true',
            'class': 'form-control',
            'placeholder': 'تاریخ پایان',
            'autocomplete': 'off',
            'style': 'font-family: Vazirmatn; font-size: 11px'
        }),
        input_formats=['%Y-%m-%d'],
        label=''
    )

    def clean_start_date(self):
        date_value = self.cleaned_data.get('start_date')
        if date_value:
            if isinstance(date_value, str):
                date_value = date_value.replace('/', '-')
                try:
                    year, month, day = map(int, date_value.split('-'))
                    return jdatetime.date(year, month, day)
                except (ValueError, TypeError):
                    raise forms.ValidationError('یک تاریخ معتبر وارد کنید.')
        return date_value

    def clean_end_date(self):
        date_value = self.cleaned_data.get('end_date')
        if date_value:
            if isinstance(date_value, str):
                date_value = date_value.replace('/', '-')
                try:
                    year, month, day = map(int, date_value.split('-'))
                    return jdatetime.date(year, month, day)
                except (ValueError, TypeError):
                    raise forms.ValidationError('یک تاریخ معتبر وارد کنید.')
        return date_value

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'manager', 'members', 'budget']
        widgets = {
            'name': forms.TextInput(attrs={
                "placeholder": "نام پروژه",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'manager': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'select2',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'budget': forms.NumberInput(attrs={
                "placeholder": "بودجه",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
        }
        labels = {
            'name': '',
            'description': '',
            'start_date': '',
            'end_date': '',
            'status': '',
            'manager': '',
            'members': '',
            'budget': '',
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
        input_formats=['%Y-%m-%d'],
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
    due_date = jDateField(
        widget=forms.TextInput(attrs={
            'data-jdp': 'true',
            'class': 'form-control',
            'placeholder': 'تاریخ سررسید',
            'autocomplete': 'off',
            'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px'
        }),
        input_formats=['%Y-%m-%d'],  # Use hyphen format as required by jDateField
        label=''
    )

    def clean_due_date(self):
        date_value = self.cleaned_data.get('due_date')
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
        model = Task
        fields = ['title', 'description', 'assigned_to', 'project', 'meeting', 'due_date', 'status', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                "placeholder": "عنوان تسک",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                "placeholder": "توضیحات",
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'project': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'meeting': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
        }
        labels = {
            'title': '',
            'description': '',
            'assigned_to': '',
            'project': '',
            'meeting': '',
            'due_date': '',
            'status': '',
            'priority': '',
        }

