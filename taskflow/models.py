from django.db import models
from django_jalali.db import models as jmodels
from accounts.models import User


# مدل جلسه
class Meeting(models.Model):
    title = models.CharField(verbose_name='موضوع', max_length=255)
    date = jmodels.jDateField(verbose_name='تاریخ', null=True, blank=True)
    notes = models.TextField(verbose_name='شرح', blank=True)
    participants = models.ManyToManyField(User, related_name='meetings', verbose_name='شرکت‌کنندگان')
    location = models.CharField(max_length=255, verbose_name='محل جلسه', blank=True, null=True)
    duration = models.IntegerField(verbose_name='مدت زمان (دقیقه)', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='meetings', verbose_name='پروژه', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.date})" if self.date else self.title



class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'در مرحله برنامه‌ریزی'),
        ('active', 'فعال'),
        ('on_hold', 'متوقف شده'),
        ('completed', 'تکمیل شده'),
        ('canceled', 'لغو شده'),
    ]

    name = models.CharField(max_length=255, verbose_name='نام پروژه')
    description = models.TextField(blank=True, default="", verbose_name='توضیحات')
    start_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ شروع")
    end_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ پایان")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', verbose_name='وضعیت')
    manager = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='managed_projects', verbose_name="مدیر پروژه")
    members = models.ManyToManyField(User, related_name='projects', verbose_name='اعضای پروژه')
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='بودجه')
    progress = models.IntegerField(default=0, verbose_name='پیشرفت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return self.name



class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'در انتظار انجام'),
        ('in_progress', 'در حال انجام'),
        ('done', 'انجام شده'),
        ('canceled', 'لغو شده'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'زیاد'),
        ('critical', 'بحرانی'),
    ]

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='موضوع')
    description = models.TextField(blank=True, default="", verbose_name='شرح')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigned_tasks', help_text="کاربری که این تسک به او محول شده")
    meeting = models.ForeignKey(Meeting, null=True, blank=True, on_delete=models.SET_NULL, related_name='meeting_tasks', help_text="اگر این تسک در یک جلسه ایجاد شده باشد، اینجا ثبت می‌شود")
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, related_name='tasks', help_text="پروژه‌ای که این تسک به آن تعلق دارد")
    due_date = jmodels.jDateField(verbose_name='تاریخ سررسید', null=True, blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='تکمیل شده')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo', verbose_name='وضعیت')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name='اولویت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ تکمیل')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks', help_text="کاربری که این تسک را ایجاد کرده")

    def __str__(self):
        return self.title if self.title else "بدون عنوان"




