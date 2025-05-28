from django.contrib import admin
from .models import Project, Meeting, Task,DailyReport
admin.site.register(Project)
admin.site.register(Meeting)
admin.site.register(Task)




@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'done_percent', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('employee__username', 'employee__first_name', 'employee__last_name', 'tasks_done', 'blockers')
    ordering = ('-date',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # هنگام ویرایش
            return ('date',)
        return ()