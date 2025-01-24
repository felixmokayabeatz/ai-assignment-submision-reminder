# In submissions/admin.py
from django.contrib import admin
from students.models import StudentSubmission
from submissions.models import Assignment

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')
    search_fields = ('title', 'course')

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at')
    list_filter = ('status', 'assignment')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from students.models import StudentProfile

class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'

class CustomUserAdmin(UserAdmin):
    inline_admin_classes = [StudentProfileInline]
    
    def get_inlines(self, request, obj=None):
        return list(super().get_inlines(request, obj)) + [StudentProfileInline]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register StudentProfile separately
admin.site.register(StudentProfile)