from django.contrib import admin
from submissions.models import StudentSubmission
from submissions.models import Assignment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from students.models import StudentProfile

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')
    search_fields = ('title', 'course')

from django.utils.html import format_html

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at', 'is_submitted', 'ai_feedback_status')
    search_fields = ('student__username', 'assignment__title')
    list_filter = ('status', 'assignment')

    # Method to display True or False for ai_feedback
    def ai_feedback_status(self, obj):
        # Check if ai_feedback exists (or is truthy), and return True or False
        return format_html('<span style="color: {};">{}</span>',
                           'green' if obj.ai_feedback else 'red',
                           'True' if obj.ai_feedback else 'False')
    ai_feedback_status.short_description = 'AI Feedback Status'


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = 'Student Profile'

class CustomUserAdmin(UserAdmin):
    inline_admin_classes = [StudentProfileInline]
    
    def get_inlines(self, request, obj=None):
        return list(super().get_inlines(request, obj)) + [StudentProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

admin.site.register(StudentProfile)