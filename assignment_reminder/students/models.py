from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    procrastination_score = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

    @receiver(post_save, sender=User)
    def create_student_profile(sender, instance, created, **kwargs):
        if created:
            StudentProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_student_profile(sender, instance, **kwargs):
        try:
            instance.student_profile.save()
        except StudentProfile.DoesNotExist:
            StudentProfile.objects.create(user=instance)

    def get_reminder_strategy(self):
        if self.procrastination_score <= -5:  # Early submitters
            return {
                'initial_reminder': 7,  # 7 days before
                'follow_up_reminders': [5, 3, 1]  # Additional reminders
            }
        elif self.procrastination_score < 0:  # Slightly early
            return {
                'initial_reminder': 5,  # 5 days before
                'follow_up_reminders': [3, 1]
            }
        elif self.procrastination_score == 0:  # Consistent
            return {
                'initial_reminder': 3,  # 3 days before
                'follow_up_reminders': [1]
            }
        elif self.procrastination_score < 5:  # Moderate procrastinator
            return {
                'initial_reminder': 2,  # 2 days before
                'follow_up_reminders': [1, 0.5]  # More frequent reminders
            }
        else:  # Extreme procrastinator
            return {
                'initial_reminder': 1,  # 1 day before
                'follow_up_reminders': [0.5, 0.25]  # Very frequent reminders
            }