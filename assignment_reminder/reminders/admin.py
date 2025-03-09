from django.contrib import admin
from submissions.models import StudentSubmission
from submissions.models import Assignment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from students.models import StudentProfile
from django.utils.html import format_html

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline')
    search_fields = ('title', 'course')

@admin.register(StudentSubmission)
class StudentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'status', 'submitted_at', 'is_submitted', 'ai_feedback_status')
    search_fields = ('student__username', 'assignment__title')
    list_filter = ('status', 'assignment')
    
    def ai_feedback_status(self, obj):
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


from students.models import Course, Unit, Enrollment, YearCategory

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_units')
    search_fields = ('name',)
    
class YearCategoryAdmin(admin.ModelAdmin):
    list_display = ['year']
    search_fields = ('year',)
    # Remove filter_horizontal since the field uses a through model


# Customizing the Unit admin view
class UnitAdmin(admin.ModelAdmin):
    list_display = ('course', 'name')  # Display the course and unit name in the list view
    search_fields = ('name',)  # Add search functionality by unit name

# Customizing the Enrollment admin view
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')  # Display student, course, and enrollment date
    search_fields = ('student__username', 'course__name')  # Search by student username and course name
    list_filter = ('course',)  # Filter by course

# Registering the models with custom admin views
admin.site.register(Course, CourseAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(YearCategory, YearCategoryAdmin)
