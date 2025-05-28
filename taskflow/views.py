from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Meeting, Project, Task,DailyReport
from django.contrib import messages
from .forms import ProjectForm, MeetingForm, TaskForm,DailyReportForm
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from django.db.models import Sum
import jdatetime





@login_required
def meeting_list(request):
    meetings = Meeting.objects.filter(participants=request.user)
    return render(request, 'taskflow/meeting_list.html', {'meetings': meetings})




# ---------------------------------------
@login_required
def meeting_detail(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk, participants=request.user)
    tasks = Task.objects.filter(meeting=meeting)
    return render(request, 'taskflow/meeting_detail.html', {
        'meeting': meeting,
        'tasks': tasks
    })


# ----------------------------------
@login_required
def meeting_create(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.save()
            form.save_m2m()

            if meeting.project:
                meeting.participants.add(*meeting.project.members.all())
            
            messages.success(request, 'جلسه با موفقیت ایجاد شد.')
            if meeting.project:
                return redirect('taskflow:project_detail', pk=meeting.project.pk)
            return redirect('taskflow:meeting_list')
        else:
            print('MeetingForm errors:', form.errors)
    else:
        initial = {}
        project_id = request.GET.get('project')
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                initial['project'] = project
                initial['participants'] = project.members.all()
            except Project.DoesNotExist:
                pass
        
        form = MeetingForm(initial=initial)
    
    return render(request, 'taskflow/meeting_form.html', {'form': form})




# ---------------------------------
@login_required
def meeting_update(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk, participants=request.user)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            messages.success(request, 'جلسه با موفقیت بروزرسانی شد.')
            if meeting.project:
                return redirect('taskflow:meeting_detail', pk=meeting.pk)
            return redirect('taskflow:meeting_list')
        else:
            print('MeetingForm errors:', form.errors)
    else:
        form = MeetingForm(instance=meeting)
    
    return render(request, 'taskflow/meeting_form.html', {
        'form': form,
        'edit_mode': True,
        'meeting': meeting
    })



# -----------------------------------
@login_required
def meeting_delete(request, pk):
    meeting = get_object_or_404(Meeting, pk=pk, participants=request.user)
    project_pk = meeting.project.pk if meeting.project else None
    meeting.delete()
    messages.success(request, 'جلسه با موفقیت حذف شد.')
    if project_pk:
        return redirect('taskflow:project_detail', pk=project_pk)
    return redirect('taskflow:meeting_list')




# ---------------------------------------
@login_required
def project_list(request):

    projects = Project.objects.all()
    return render(request, 'taskflow/project_list.html', {'projects': projects})



# --------------------------------------
@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not (request.user.is_superuser or project.manager == request.user):
        messages.error(request, 'شما دسترسی لازم برای مشاهده جزئیات این پروژه را ندارید.')
        return redirect('taskflow:project_list')
    meetings = Meeting.objects.filter(project=project)
    meetings_with_tasks = []
    for meeting in meetings:
        tasks = Task.objects.filter(meeting=meeting, project=project)
        meetings_with_tasks.append({
            'meeting': meeting,
            'tasks': tasks
        })

        # تبدیل تاریخ شروع و پایان پروژه به جلالی
    jalali_start_date = None
    if project.start_date:
        jalali_start_date = jdatetime.date.fromgregorian(date=project.start_date).strftime('%Y/%m/%d')

    jalali_end_date = None
    if project.end_date:
        jalali_end_date = jdatetime.date.fromgregorian(date=project.end_date).strftime('%Y/%m/%d')
    return render(request, 'taskflow/project_detail.html', {
        'project': project,
        'meetings_with_tasks': meetings_with_tasks,
        'jalali_start_date': jalali_start_date,
        'jalali_end_date': jalali_end_date,
    })




# ------------------------------------
@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            form.save_m2m()
            messages.success(request, 'پروژه با موفقیت ایجاد شد.')
            return redirect('taskflow:project_list')
        else:
            print('ProjectForm errors:', form.errors)
    else:
        form = ProjectForm()
    
    return render(request, 'taskflow/project_form.html', {'form': form})




# --------------------------------------
@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk, members=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            messages.success(request, 'پروژه با موفقیت بروزرسانی شد.')
            return redirect('taskflow:project_detail', pk=project.pk)
        else:
            print('ProjectForm errors:', form.errors)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'taskflow/project_form.html', {
        'form': form,
        'edit_mode': True,
        'project': project
    })



# ----------------------------------
@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, members=request.user)
    project.delete()
    messages.success(request, 'پروژه با موفقیت حذف شد.')
    return redirect('taskflow:project_list')



# ---------------------------------------
@login_required
def task_list(request):
    status = request.GET.get('status')
    if status == 'all':
        tasks = Task.objects.filter(assigned_to=request.user)
    elif status in ['todo', 'in_progress', 'done', 'canceled']:
        tasks = Task.objects.filter(assigned_to=request.user, status=status)
    else:
        tasks = Task.objects.filter(assigned_to=request.user, status__in=['todo', 'in_progress'])
    waiting_tasks = Task.objects.filter(assigned_to=request.user, status='waiting_approval')
    projects = Project.objects.filter(members=request.user)
    users = User.objects.all()
    return render(request, 'taskflow/task_list.html', {
        'tasks': tasks,
        'waiting_tasks': waiting_tasks,
        'projects': projects,
        'users': users,
        'selected_status': status or 'active',
    })


# ---------------------------------------
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'taskflow/task_detail.html', {'task': task})


# ----------------------------------------
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            form.save_m2m()
            messages.success(request, 'تسک با موفقیت ایجاد شد.')
            return redirect('taskflow:task_list')
        else:
            print('TaskForm errors:', form.errors)
    else:
        initial = {}
        project_id = request.GET.get('project')
        if project_id:
            try:
                project = Project.objects.get(id=project_id)
                initial['project'] = project
            except Project.DoesNotExist:
                pass
        
        form = TaskForm(initial=initial)
    
    return render(request, 'taskflow/task_form.html', {'form': form})



# -----------------------------------------
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'تسک با موفقیت بروزرسانی شد.')
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse('')
            return redirect('taskflow:task_detail', pk=task.pk)
        else:
            print('TaskForm errors:', form.errors)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return render(request, 'taskflow/task_form.html', {'form': form, 'edit_mode': True, 'task': task})
    else:
        form = TaskForm(instance=task)
    return render(request, 'taskflow/task_form.html', {'form': form, 'edit_mode': True, 'task': task})



# -------------------------------------------
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    messages.success(request, 'تسک با موفقیت حذف شد.')
    return redirect('taskflow:task_list')


@login_required
def get_project_meetings(request):
    project_id = request.GET.get('project_id')
    if project_id:
        meetings = Meeting.objects.filter(project_id=project_id)
        meetings_list = [{'id': meeting.id, 'title': meeting.title} for meeting in meetings]
        return JsonResponse({'meetings': meetings_list})
    return JsonResponse({'meetings': []})

# ======================================
def get_persian_weekday_name(jdate):
    weekdays = {
        'شنبه': 'شنبه',
        'یکشنبه': 'یکشنبه',
        'دوشنبه': 'دوشنبه',
        'سه شنبه': 'سه‌شنبه',
        'چهارشنبه': 'چهارشنبه',
        'پنجشنبه': 'پنج‌شنبه',
        'جمعه': 'جمعه',
    }
    raw_weekday = jdate.strftime('%A')
    cleaned_weekday = raw_weekday.replace('\u200c', ' ').strip()
    return weekdays.get(cleaned_weekday, cleaned_weekday)
# -----------------------------------
@login_required
def daily_report_list(request):
    reports = DailyReport.objects.all().select_related('employee').order_by('-date', '-created_at')
    today = jdatetime.date.today()
    weekday_name = get_persian_weekday_name(today)
    # جمع دقیقه‌ها برای هر تاریخ
    daily_durations = (
        DailyReport.objects
        .values('date')
        .annotate(total_minutes=Sum('duration_minutes'))
        .order_by('-date')
    )
    return render(request, 'taskflow/daily_report_list.html', {'reports': reports ,'weekday_name': weekday_name,
        'today': today,'daily_durations': daily_durations,})
# -----------------------------------------


@login_required
def daily_report_create(request):
    today = jdatetime.date.today()
    weekday_name = get_persian_weekday_name(today)
    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.employee = request.user
            report.date = today  # همان today که بالا تعریف شده
            report.save()
            messages.success(request, 'گزارش جدید با موفقیت ثبت شد.')
            return redirect('taskflow:daily_report_list')
        else:
            print('DailyReportForm errors:', form.errors)
    else:
        form = DailyReportForm()

    return render(request, 'taskflow/daily_report_create.html', {
        'form': form,
        'weekday_name': weekday_name,  # ارسال روز هفته به قالب
        'today': today,  # ارسال تاریخ امروز به قالب
        'user': request.user,
    })


# ---------------------------------------------