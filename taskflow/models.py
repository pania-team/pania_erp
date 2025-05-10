from django.db import models
from django_jalali.db import models as jmodels
from accounts.models import User








# مدل جلسه
class Meeting(models.Model):
    title = models.CharField(verbose_name='موضوع',max_length=255)
    date = jmodels.jDateField(verbose_name='تاریخ', null=True, blank=True)
    notes = models.TextField(verbose_name='شرح',blank=True)
    participants = models.ManyToManyField(User, related_name='meetings')

    def __str__(self):
        return f"{self.title} ({self.date})" if self.date else self.title



class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    start_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ شروع")
    end_date = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ پایان")
    members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.name



class Task(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True,verbose_name='موضوع')
    description = models.TextField(blank=True, default="",verbose_name='شرح')
    assigned_to = models.ForeignKey(User,on_delete=models.PROTECT,related_name='assigned_tasks',
        help_text="کاربری که این تسک به او محول شده")
    meeting = models.ForeignKey(Meeting, null=True,blank=True,on_delete=models.SET_NULL,related_name='meeting_tasks',
        help_text="اگر این تسک در یک جلسه ایجاد شده باشد، اینجا ثبت می‌شود")
    project = models.ForeignKey(
        Project, null=True, blank=True, on_delete=models.CASCADE,
        related_name='tasks',
        help_text="پروژه‌ای که این تسک به آن تعلق دارد"
    )

    due_date = jmodels.jDateField(verbose_name='تاریخ', null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True,related_name='created_tasks',
        help_text="کاربری که این تسک را ایجاد کرده" )


    def __str__(self):
        return self.title if self.title else "بدون عنوان"




