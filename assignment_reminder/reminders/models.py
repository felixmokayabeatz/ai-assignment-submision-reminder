from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    procrastination_level = models.IntegerField(default=5)  # Scale 1-10

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reminder_sent = models.BooleanField(default=False)

class Reminder(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField()
    sent = models.BooleanField(default=False)
