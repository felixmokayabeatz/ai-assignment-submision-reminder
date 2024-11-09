from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Assignment, Reminder

def send_reminder(student, assignment):
    send_mail(
        f"Reminder: {assignment.title} Due Soon!",
        f"Hi {student.name}, your assignment '{assignment.title}' is due on {assignment.due_date}.",
        'no-reply@school.com',
        [student.email],
    )

def schedule_reminders():
    assignments = Assignment.objects.all()
    for assignment in assignments:
        days_left = (assignment.due_date - datetime.now()).days
        if days_left <= 3:  # Customize this based on behavior model
            send_reminder(assignment.student, assignment)
