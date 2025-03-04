import os
import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from submissions.models import Assignment, StudentSubmission
from django.shortcuts import render, get_object_or_404

now = timezone.now()

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../submissions/reminder_model.pkl")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")


with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)
    
def home(request):
    return render(request, 'home/home.html')

@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user
    submission, created = StudentSubmission.objects.get_or_create(student=student, assignment=assignment)

    if request.method == "POST":
        now = timezone.now()
        submission.submitted_at = now
        submission.is_submitted = True  

        if now < assignment.deadline:
            time_difference = (assignment.deadline - now).total_seconds()
            if time_difference > 86400:
                submission.status = StudentSubmission.SubmissionStatus.SUBMITTED_EARLY
            else:
                submission.status = StudentSubmission.SubmissionStatus.SUBMITTED_ON_TIME
        else:
            submission.status = StudentSubmission.SubmissionStatus.LATE_SUBMISSION
        
        submission.save()
        messages.success(request, "Assignment submitted successfully!")
        return redirect("assignment_list")

    return render(request, "submit_assignment.html", {"assignment": assignment, "submission": submission})

@login_required
def assignment_list(request):    
    student = request.user
    assignments = Assignment.objects.all()
    submissions = {sub.assignment.id: sub for sub in StudentSubmission.objects.filter(student=student)}

    completed_assignments = sum(1 for sub in submissions.values() if sub.is_submitted)
    unsubmitted_assignments = [assignment for assignment in assignments if assignment.id not in submissions]

    now = timezone.now()
    assignments_deadline = Assignment.objects.filter(
        deadline__gte=now,
        deadline__lte=now + timezone.timedelta(days=7)
    ).exclude(id__in=[aid for aid, sub in submissions.items() if sub.is_submitted])

    return render(request, "assignment_list.html", {
        "assignments": assignments,
        "submissions": submissions,
        "completed_assignments": completed_assignments,
        "unsubmitted_assignments": unsubmitted_assignments,
        "assignments_deadline": assignments_deadline
    })
