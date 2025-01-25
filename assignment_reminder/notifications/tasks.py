from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User

@shared_task
def send_assignment_reminders():
    from submissions.models import Assignment, StudentSubmission
    from students.models import StudentProfile

    print("Task executed!")

    # Get upcoming assignments within the next 7 days
    upcoming_assignments = Assignment.objects.filter(
        deadline__range=[timezone.now(), timezone.now() + timezone.timedelta(days=7)]
    )
    print(f"Found {upcoming_assignments.count()} assignments.")

    for assignment in upcoming_assignments:
        student_submissions = StudentSubmission.objects.filter(
            assignment=assignment,
            is_submitted=False
        )
        print(f"Processing {student_submissions.count()} submissions for {assignment.title}.")

        for submission in student_submissions:
            # Fetch the User object if submission.student is not a User instance
            if isinstance(submission.student, str):
                try:
                    student = User.objects.get(username=submission.student)
                except User.DoesNotExist:
                    print(f"Error: User with username {submission.student} does not exist.")
                    continue
            else:
                student = submission.student  # Already a User object

            # Fetch the reminder strategy and calculate the days until deadline
            student_profile = StudentProfile.objects.get(user=student)
            reminder_strategy = student_profile.get_reminder_strategy()
            days_until_deadline = (assignment.deadline - timezone.now()).days

            print(f"Days until deadline for {assignment.title}: {days_until_deadline}")
            print(f"Reminder strategy for {student.username}: {reminder_strategy['follow_up_reminders']}")

            # Check if it's time to send a reminder
            if days_until_deadline in reminder_strategy['follow_up_reminders'] or days_until_deadline == 0:
                send_reminder_email(
                    student,  # Pass the User object directly
                    assignment,
                    days_until_deadline
                )
                print(f"Email sent for {assignment.title} to {student.username}.")
            else:
                print(f"Not time to send reminder for {assignment.title} to {student.username}.")
                
    return "Task finished"




def send_reminder_email(user, assignment, days_until_deadline):
    subject = f"Reminder: Assignment '{assignment.title}' Due in {days_until_deadline} Days"
    message = (
        f"Dear {user.first_name},\n\n"
        f"The assignment '{assignment.title}' is due on {assignment.deadline.strftime('%Y-%m-%d %H:%M')}.\n"
        f"Please make sure to submit it on time.\n\n"
        "Best regards,\nYour School Team"
    )
    recipient_list = [user.email]
    send_mail(subject, message, 'felixmokayabeatz@gmail.com', recipient_list)


