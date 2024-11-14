from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.shortcuts import render
import joblib
import os
from django.conf import settings
from .models import Assignment, Reminder, Student
from .tasks import check_and_send_reminders
from django.contrib.auth.decorators import login_required
from django.utils import timezone


# Load the trained model
model_path = os.path.join(settings.BASE_DIR, 'reminders', 'model', 'reminder_model.pkl')
model = joblib.load(model_path)

@login_required
def predict_submission(request):
    check_and_send_reminders.apply_async()  # This will run the task asynchronously

    if request.method == 'POST':
        # Get the logged-in student's assignments
        student = Student.objects.get(user=request.user)
        assignment = Assignment.objects.filter(student=student).first()  # Get the first assignment for simplicity

        if assignment:
            days_before_due = (assignment.due_date - timezone.now()).days
            reminders_sent = Reminder.objects.filter(assignment=assignment, student=student, sent=True).count()

            # Prepare data for prediction
            new_data = [[days_before_due, reminders_sent]]
            prediction = model.predict(new_data)[0]

            # Map prediction to status
            status = "On Time" if prediction == 1 else "Late"
            
            return render(request, 'prediction.html', {'status': status, 'assignment': assignment})

    return render(request, 'prediction.html', {'status': 'No assignment found'})


def send_reminder(student, assignment):
    send_mail(
        f"Reminder: {assignment.title} Due Soon!",
        f"Hi {student.user.username}, your assignment '{assignment.title}' is due on {assignment.due_date}.",
        'no-reply@school.com',
        [student.user.email],
    )


def schedule_reminders():
    assignments = Assignment.objects.all()
    for assignment in assignments:
        days_left = (assignment.due_date - timezone.now()).days
        if days_left <= 3:  # Customize this based on behavior model
            send_reminder(assignment.student, assignment)
