from django.db import models
from django_jalali.db import models as jmodels
from accounts.models import User
import jdatetime




# -------------------------
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
    budget = models.IntegerField(null=True, blank=True, verbose_name='بودجه')
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
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks', verbose_name='مسئولین', help_text="کاربرانی که این تسک به آن‌ها محول شده")
    meeting = models.ForeignKey(Meeting, null=True, blank=True, on_delete=models.CASCADE, related_name='meeting_tasks', help_text="اگر این تسک در یک جلسه ایجاد شده باشد، اینجا ثبت می‌شود")
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

# ---------------------------------------


class DailyReport(models.Model):
    STATUS_CHOICES = [
        ('completed', 'انجام شده'),
        ('in_progress', 'در حال انجام'),
    ]
    employee = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کارمند")
    date = jmodels.jDateField(verbose_name="تاریخ")
    tasks_done = models.CharField(max_length=255,verbose_name="کارهای انجام‌شده")
    duration_minutes = models.PositiveIntegerField(blank=True, null=True, verbose_name="مدت زمان (دقیقه)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed',
                              verbose_name="وضعیت انجام کار")
    done_percent = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="درصد انجام")
    blockers = models.CharField(max_length=255, blank=True, null=True, verbose_name="مشکلات یا موانع")
    suggestions = models.CharField(max_length=255, blank=True, null=True, verbose_name="پیشنهادات")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "گزارش روزانه"
        verbose_name_plural = "گزارش‌های روزانه"

    def __str__(self):
        return f"{self.employee} - {self.date}"


    @property
    def weekday_name(self):
        if self.date:
            weekdays = {
                'Saturday': 'شنبه',
                'Sunday': 'یکشنبه',
                'Monday': 'دوشنبه',
                'Tuesday': 'سه‌شنبه',
                'Wednesday': 'چهارشنبه',
                'Thursday': 'پنج‌شنبه',
                'Friday': 'جمعه',
            }
            # اطمینان از اینکه date از نوع jDate هست
            if isinstance(self.date, jdatetime.date):
                return weekdays[self.date.strftime('%A')]
            else:
                # تبدیل میلادی به جلالی در صورت نیاز
                jdate = jdatetime.date.fromgregorian(date=self.date)
                return weekdays[jdate.strftime('%A')]
        return ''

# -----------------------------------------
import datetime
from django_jalali.db import models as jmodels


class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('daily_leave', 'مرخصی روزانه'),
        ('hourly_leave', 'مرخصی ساعتی'),
        ('daily_mission', 'ماموریت روزانه'),
        ('hourly_mission', 'ماموریت ساعتی'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    leave_date = jmodels.jDateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-leave_date']

    def duration_hours(self):
        if self.leave_type in ['hourly_leave', 'hourly_mission'] and self.start_time and self.end_time:
            delta = datetime.datetime.combine(datetime.date.min, self.end_time) - datetime.datetime.combine(datetime.date.min, self.start_time)
            return round(delta.total_seconds() / 3600, 2)
        return 0
# ----------------------------------------------