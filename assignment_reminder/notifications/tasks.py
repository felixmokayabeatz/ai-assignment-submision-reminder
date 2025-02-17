from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.timezone import make_aware, localtime
from django.contrib.auth.models import User

@shared_task
def send_assignment_reminders():
    from submissions.models import Assignment, StudentSubmission
    from students.models import StudentProfile
    
    print("Task executed!")
    
    now_utc = timezone.now()
    
    upcoming_assignments = Assignment.objects.filter(
        deadline__range=[now_utc, now_utc + timezone.timedelta(days=7)]
    ).select_related('course')  # Add select_related if there's a course relation
    
    print(f"Found {upcoming_assignments.count()} assignments.")
    
    for assignment in upcoming_assignments:
        # Ensure deadline is in UTC
        deadline = assignment.deadline
        if deadline.tzinfo is None:
            deadline = make_aware(deadline, timezone.utc)
        
        student_submissions = StudentSubmission.objects.filter(
            assignment=assignment,
            is_submitted=False
        ).select_related('student')  # Optimize by pre-fetching student data
        
        print(f"Processing {student_submissions.count()} submissions for {assignment.title}.")
        
        for submission in student_submissions:
            try:
                # Get student user object
                student = (
                    submission.student if isinstance(submission.student, User)
                    else User.objects.get(username=submission.student)
                )
                
                # Get student profile and reminder strategy
                student_profile = StudentProfile.objects.get(user=student)
                reminder_strategy = student_profile.get_reminder_strategy()
                
                # Calculate days until deadline in UTC
                time_until_deadline = deadline - now_utc
                days_until_deadline = time_until_deadline.days
                
                print(f"Days until deadline for {assignment.title}: {days_until_deadline}")
                print(f"Reminder strategy for {student.username}: {reminder_strategy['follow_up_reminders']}")
                
                # Check if reminder should be sent
                if days_until_deadline in reminder_strategy['follow_up_reminders'] or days_until_deadline == 0:
                    # Convert deadline to student's local timezone for email
                    local_deadline = localtime(deadline)
                    
                    send_reminder_email(
                        student,
                        assignment,
                        days_until_deadline,
                        local_deadline=local_deadline  # Pass localized deadline to email function
                    )
                    print(f"Email sent for {assignment.title} to {student.username}.")
                else:
                    print(f"Not time to send reminder for {assignment.title} to {student.username}.")
                    
            except User.DoesNotExist:
                print(f"Error: User with username {submission.student} does not exist.")
                continue
            except Exception as e:
                print(f"Error processing submission for {assignment.title}: {str(e)}")
                continue
    
    return "Task finished"

def send_reminder_email(user, assignment, days_until_deadline):
    subject = f"Reminder: Assignment '{assignment.title}' Due in {days_until_deadline} Days"
    message = (
        f"Dear {user.first_name},\n\n"
        f"The assignment '{assignment.title}' is due on {localtime(assignment.deadline).strftime('%Y-%m-%d %H:%M')} (your local time).\n"
        f"Please make sure to submit it on time.\n\n"
        "Best regards,\nYour School Team"
    )
    recipient_list = [user.email]
    send_mail(subject, message, 'felixmokayabeatz@gmail.com', recipient_list)
