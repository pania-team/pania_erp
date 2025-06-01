from django.contrib import admin
from .models import Project, Meeting, Task,DailyReport
admin.site.register(Project)
admin.site.register(Meeting)
admin.site.register(Task)




@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'done_percent', 'tasks_done', 'duration_minutes')
    list_filter = ('status', 'date')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name', 'tasks_done', 'blockers')
    ordering = ('-date',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # هنگام ویرایش
            return ('date',)
        return ()

# --------------------------------------------
from django.contrib import admin
from .models import LeaveRequest

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'leave_type',
        'leave_date',
        'start_time',
        'end_time',
        'approved_by_supervisor',
        'supervisor',
        'approved_at',
    )
    list_filter = ('leave_type', 'leave_date', 'approved_by_supervisor')
    search_fields = ('user__username', 'description', 'supervisor__username')
    date_hierarchy = 'leave_date'
    ordering = ('-leave_date',)

