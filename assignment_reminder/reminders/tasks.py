# reminders/tasks.py

import logging
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from celery import shared_task

from .models import Assignment  # Adjust according to your model location

logger = logging.getLogger(__name__)
@shared_task
def check_and_send_reminders():
    now = timezone.now()
    # Fetch assignments that are due within 3 days and haven't been sent reminders yet
    upcoming_assignments = Assignment.objects.filter(due_date__lte=now + timedelta(days=3), reminder_sent=False)

    for assignment in upcoming_assignments:
        logger.info(f"Sending reminder for {assignment.title} due on {assignment.due_date}")
        send_mail(
            'Reminder: Upcoming Assignment Due',
            f'Your assignment "{assignment.title}" is due soon. Due date is {assignment.due_date}',
            'ecopiboe@gmail.com',  # Replace with your actual sender email
            [assignment.student.user.email],  # Assuming you have a related student field on Assignment
            fail_silently=False,
        )
        assignment.reminder_sent = True  # Mark reminder as sent
        assignment.save()  # Save the change
        logger.info(f"Reminder sent for {assignment.title}")
