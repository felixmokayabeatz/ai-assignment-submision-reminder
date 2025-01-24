# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import logging

@shared_task
def send_assignment_reminders():
    # Delayed import to prevent AppRegistryNotReady error
    from submissions.models import Assignment, StudentSubmission
    from students.models import StudentProfile
    
    print("Task executed!")

    # Get upcoming assignments within the next 7 days
    upcoming_assignments = Assignment.objects.filter(
        deadline__range=[timezone.now(), timezone.now() + timezone.timedelta(days=7)]
    )
    
    for assignment in upcoming_assignments:
        # Find students enrolled in this assignment
        student_submissions = StudentSubmission.objects.filter(
            assignment=assignment, 
            is_submitted=False
        )
        
        for submission in student_submissions:
            student_profile = StudentProfile.objects.get(user=submission.student)
            reminder_strategy = student_profile.get_reminder_strategy()
            
            # Calculate days until deadline
            days_until_deadline = (assignment.deadline - timezone.now()).days
            
            # Check if it's time to send a reminder
            if days_until_deadline in reminder_strategy['follow_up_reminders']:
                send_reminder_email(
                    submission.student, 
                    assignment, 
                    days_until_deadline
                )
        return "Task finished"


def send_reminder_email(student, assignment, days_left):
    try:
        send_mail(
            subject=f'Upcoming Assignment Deadline: {assignment.title}',
            message=f'Hi {student.first_name},\n\nThis is a reminder about your upcoming assignment: {assignment.title}\n\n',
            from_email='felixmokayabeatz@gmail.com',
            recipient_list=[student.email],
            fail_silently=False
        )
    except Exception as e:
        logging.error(f"Failed to send email to {student.email}: {e}")
