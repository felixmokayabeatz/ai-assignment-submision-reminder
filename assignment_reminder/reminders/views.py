import os
import pickle
import numpy as np
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from submissions.models import Assignment, StudentSubmission
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Go one level up
# MODEL_PATH = os.path.join(BASE_DIR, "submissions", "reminder_model.pkl")

import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../submissions/reminder_model.pkl")

print(MODEL_PATH)

# Load the trained model
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


@login_required
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user
    submission, created = StudentSubmission.objects.get_or_create(student=student, assignment=assignment)

    if request.method == "POST":
        submission.submitted_at = timezone.now()
        submission.is_submitted = True
        submission.save()
        messages.success(request, "Assignment submitted successfully!")
        return redirect("assignment_list")

    return render(request, "submit_assignment.html", {"assignment": assignment, "submission": submission})



@login_required
def assignment_list(request):
    assignments = Assignment.objects.all()
    return render(request, "home/assignment_list.html", {"assignments": assignments})
