from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_units = models.IntegerField(default=7)  # Default max units
    students = models.ManyToManyField(User, through='Enrollment', related_name='enrolled_courses')

    def __str__(self):
        return self.name

class YearCategory(models.Model):
    year = models.IntegerField(choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')])

    def __str__(self):
        return f"Year {self.year}"
    
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=255)
    content = models.TextField()
    available_for_years = models.ManyToManyField(YearCategory, related_name='available_units', blank=True)

    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.name}"




class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    procrastination_score = models.FloatField(default=0)
    submission_history = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def enrolled_courses(self):
        """Return a list of courses the student is enrolled in."""
        return self.user.enrolled_courses.all()

    def get_reminder_strategy(self):
        """Determine reminder strategy based on procrastination score."""
        if self.procrastination_score <= -5:
            return {'initial_reminder': 7, 'follow_up_reminders': [5, 3, 1]}
        elif self.procrastination_score < 0:
            return {'initial_reminder': 5, 'follow_up_reminders': [3, 1]}
        elif self.procrastination_score == 0:
            return {'initial_reminder': 3, 'follow_up_reminders': [1]}
        elif self.procrastination_score < 5:
            return {'initial_reminder': 2, 'follow_up_reminders': [1, 0.5]}
        else:
            return {'initial_reminder': 1, 'follow_up_reminders': [0.5, 0.25]}

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    """Automatically create StudentProfile when a new user is created."""
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    try:
        instance.student_profile.save()
    except StudentProfile.DoesNotExist:
        StudentProfile.objects.create(user=instance)

def get_reminder_strategy(self):
    if self.procrastination_score <= -5:
        return {
            'initial_reminder': 7,
            'follow_up_reminders': [5, 3, 1]
        }
    elif self.procrastination_score < 0:
        return {
            'initial_reminder': 5,
            'follow_up_reminders': [3, 1]
        }
    elif self.procrastination_score == 0:
        return {
            'initial_reminder': 3,
            'follow_up_reminders': [1]
        }
    elif self.procrastination_score < 5:
        return {
            'initial_reminder': 2,
            'follow_up_reminders': [1, 0.5]
        }
    else:
        return {
            'initial_reminder': 1,
            'follow_up_reminders': [0.5, 0.25]
        }