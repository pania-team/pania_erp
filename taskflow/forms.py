from django import forms
from .models import Project, Meeting, Task, DailyReport,LeaveRequest
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('', 'وضعیت پروژه')] + list(self.fields['status'].choices)
        self.fields['manager'].empty_label = "مدیر پروژه"
        self.fields['manager'].required = True

        if not self.initial.get('status') and not self.data.get('status'):
            self.initial['status'] = ''
        
    def clean_manager(self):
        manager = self.cleaned_data.get('manager')
        if not manager:
            raise forms.ValidationError('انتخاب مدیر پروژه الزامی است.')
        return manager

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
                'placeholder': 'وضعیت پروژه ',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'manager': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'مدیر پروژه ',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            'members': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'اعضای پروژه',
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
        fields = ['title', 'date', 'location', 'duration', 'notes', 'participants']
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
            'participants': forms.SelectMultiple(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
        }
        labels = {
            'title': '',
            'date': '',
            'location': '',
            'duration': '',
            'notes': '',
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = [('', 'وضعیت تسک')] + list(self.fields['status'].choices)
        self.fields['priority'].choices = [('', 'اولویت تسک')] + list(self.fields['priority'].choices)
        # مقدار پیش‌فرض برای اولویت (مثلاً 'medium' یا هر مقدار دلخواه)
        if not self.initial.get('priority') and not self.data.get('priority'):
            self.initial['priority'] = 'اولویت تسک'
            self.initial['status'] = 'وضعیت تسک'
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'priority']
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
            'assigned_to': forms.SelectMultiple(attrs={
                'class': 'form-control',
                "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            }),
            # 'project': forms.Select(attrs={
            #     'class': 'form-control',
            #     "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            # }),
            # 'meeting': forms.Select(attrs={
            #     'class': 'form-control',
            #     "style": "font-family: Vazirmatn, sans-serif; font-size: 11px"
            # }),
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

# ---------------------------------

#
class DailyReportForm(forms.ModelForm):
    class Meta:
        model = DailyReport
        exclude = ['date']
        fields = ['tasks_done','duration_minutes',  'status', 'done_percent','blockers', 'suggestions']
        widgets = {
            'tasks_done': forms.TextInput(attrs={
                'placeholder': 'فعالیت انجام‌شده',
                'style': 'font-family: Vazirmatn; font-size: 11px',
                'required': True,
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'placeholder': 'مدت زمان (دقیقه)',
                'class': 'form-control',
                'style': 'font-family: Vazirmatn; font-size: 11px',
                'min': '0',
                'max': '480',
                'required': True,
            }),
            'blockers': forms.TextInput(attrs={
                'placeholder': 'مشکلات یا موانع (اختیاری)',
                'style': 'font-family: Vazirmatn; font-size: 11px'
            }),
            'suggestions': forms.TextInput(attrs={
                'placeholder': 'پیشنهادات (اختیاری)',
                'style': 'font-family: Vazirmatn; font-size: 11px'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-family: Vazirmatn; font-size: 11px',
                'required': True,
            }),
            'done_percent': forms.NumberInput(attrs={
                'placeholder': 'درصد انجام کار',
                'class': 'form-control',
                'style': 'font-family: Vazirmatn; font-size: 11px',
                'min': '0',
                'max': '100',
               'required': True,
            }),
        }
        labels = {
            'date': '',
            'tasks_done': '',
            'duration_minutes':'',
            'blockers': '',
            'suggestions': '',
            'status': '',
            'done_percent': '',
        }

# ---------------------------------------------------

class DailyLeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'leave_date', 'description']
        widgets = {
            'leave_type': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'leave_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ مرخصی یا ماموریت',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
                'autocomplete': 'off',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح مرخصی یا ماموریت',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
            }),
        }
        labels = {
            'leave_type': '',
            'leave_date': '',
            'description': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # فقط گزینه‌های روزانه را در leave_type نمایش بده
        self.fields['leave_type'].choices = [
            choice for choice in LeaveRequest.LEAVE_TYPES
            if choice[0] in ['daily_leave', 'daily_mission']
        ]

# -----------------------------------
import datetime

class HourlyLeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'leave_date', 'start_time', 'end_time', 'description']
        widgets = {
            'leave_type': forms.Select(attrs={
                'class': 'form-control',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 12px;',
            }),
            'leave_date': forms.TextInput(attrs={
                'data-jdp': 'true',
                'class': 'form-control',
                'required': True,
                'placeholder': 'تاریخ مرخصی یا ماموریت',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
                'autocomplete': 'off',
            }),
            'start_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'ساعت شروع',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
            }),
            'end_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'ساعت پایان',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شرح مرخصی یا ماموریت',
                'style': 'font-family: Vazirmatn, sans-serif; font-size: 11px',
            }),
        }
        labels = {
            'leave_type': '',
            'leave_date': '',
            'start_time': '',
            'end_time': '',
            'description': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # فقط گزینه‌های ساعتی را در leave_type نمایش بده
        self.fields['leave_type'].choices = [
            choice for choice in LeaveRequest.LEAVE_TYPES
            if choice[0] in ['hourly_leave', 'hourly_mission']
        ]

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        leave_type = cleaned_data.get('leave_type')

        if leave_type in ['hourly_leave', 'hourly_mission'] and start_time and end_time:
            # از datetime.datetime استاندارد استفاده کن چون فقط محاسبه اختلاف زمانی است
            start_dt = datetime.datetime.combine(datetime.date.today(), start_time)
            end_dt = datetime.datetime.combine(datetime.date.today(), end_time)
            delta = end_dt - start_dt
            duration_hours = delta.total_seconds() / 3600

            if duration_hours <= 0:
                raise forms.ValidationError("ساعت پایان باید بعد از ساعت شروع باشد.")
            if duration_hours > 4:
                raise forms.ValidationError("مدت مرخصی ساعتی نمی‌تواند بیش از ۴ ساعت باشد.")

# --------------------------------------