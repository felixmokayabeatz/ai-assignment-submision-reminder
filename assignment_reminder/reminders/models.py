from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    procrastination_level = models.IntegerField(default=5)  # Scale 1-10

    def __str__(self):
        return self.user.username


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reminder_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"Reminder for {self.assignment.title} to {self.student.user.username}"
