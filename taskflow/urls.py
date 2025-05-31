from django.urls import path
from . import views

app_name = 'taskflow'
urlpatterns = [
    # Meeting URLs
    path('meeting_list/', views.meeting_list, name='meeting_list'),
    path('meeting_create/', views.meeting_create, name='meeting_create'),
    path('meeting_detail/<int:pk>/', views.meeting_detail, name='meeting_detail'),
    path('meeting_update/<int:pk>/edit/', views.meeting_update, name='meeting_update'),
    path('meeting_delete/<int:pk>/delete/', views.meeting_delete, name='meeting_delete'),

    # Project URLs
    path('project_list/', views.project_list, name='project_list'),
    path('project_create/', views.project_create, name='project_create'),
    path('project_detail/<int:pk>/', views.project_detail, name='project_detail'),
    path('project_update/<int:pk>/edit/', views.project_update, name='project_update'),
    path('project_delete/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project_tasks/<int:pk>/', views.project_tasks_view, name='project_tasks'),

    # Task URLs
    path('task_list/', views.task_list, name='task_list'),
    path('task_create/create/', views.task_create, name='task_create'),
    path('task_detail/<int:pk>/', views.task_detail, name='task_detail'),
    path('task_update/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task_delete/<int:pk>/delete/', views.task_delete, name='task_delete'),


    path('get-project-meetings/', views.get_project_meetings, name='get_project_meetings'),

    # Report Url
    path('daily-report-create/create/', views.daily_report_create, name='daily_report_create'),
    path('daily-report-list/', views.daily_report_list, name='daily_report_list'),
    path('employee_report_list/', views.employee_report_list, name='employee_report_list'),
    # Leave Url
    path('leave-dashboard/', views.leave_dashboard, name='leave_dashboard'),
]