from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Assignment, Reminder


from django.shortcuts import render
import joblib
import os
from django.conf import settings
# views.py
from .tasks import check_and_send_reminders

model_path = os.path.join(settings.BASE_DIR, 'reminders', 'model', 'reminder_model.pkl')
model = joblib.load(model_path)

def predict_submission(request):
    check_and_send_reminders.apply_async()  # This will run the task asynchronously
    if request.method == 'POST':
        days_before_due = int(request.POST.get('days_before_due'))
        reminders_sent = int(request.POST.get('reminders_sent'))
        
        # Prepare data for prediction
        new_data = [[days_before_due, reminders_sent]]
        prediction = model.predict(new_data)[0]
        
        # Map prediction to status
        status = "On Time" if prediction == 1 else "Late"
        
        return render(request, 'prediction.html', {'status': status})
    
    return render(request, 'prediction.html')

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




# def predict_submission(request):
#     check_and_send_reminders.apply_async()  # This will run the task asynchronously
#     return render(request, 'prediction.html')
