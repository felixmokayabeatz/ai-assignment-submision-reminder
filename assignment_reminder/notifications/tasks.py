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
        deadline__range=[now_utc, now_utc + timezone.timedelta(days=10)]
    )

    print(f"Found {upcoming_assignments.count()} assignments.")

    pending_submissions = []  # ✅ Initialize pending_submissions

    for assignment in upcoming_assignments:
        deadline = assignment.deadline
        if deadline.tzinfo is None:
            deadline = make_aware(deadline, timezone.utc)

        # Get only students who haven't submitted yet
        pending_submissions.extend(
            StudentSubmission.objects.filter(
                assignment=assignment,
                is_submitted=False
            ).select_related('student')
        )

        print(f"Processing {len(pending_submissions)} pending submissions for {assignment.title}.")

    # ✅ Ensure we have pending submissions before iterating
    if not pending_submissions:
        print("No pending submissions found.")
        return "No reminders to send"

    for submission in pending_submissions:
        try:
            student = submission.student
            if isinstance(student, str):  # Handle case where student is stored as a username
                student = User.objects.get(username=student)

            # ✅ Double-check submission status before proceeding
            if submission.is_submitted:
                print(f"Skipping {student.username}, already submitted {assignment.title}.")
                continue  # Skip sending email

            student_profile = StudentProfile.objects.get(user=student)
            reminder_strategy = student_profile.get_reminder_strategy()
            
            time_until_deadline = deadline - now_utc
            days_until_deadline = time_until_deadline.days

            print(f"Days until deadline for {assignment.title}: {days_until_deadline}")
            print(f"Reminder strategy for {student.username}: {reminder_strategy['follow_up_reminders']}")

            if days_until_deadline in reminder_strategy['follow_up_reminders'] or days_until_deadline <= 3:
                local_deadline = localtime(deadline)
                
                send_reminder_email(student, assignment, days_until_deadline)
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
