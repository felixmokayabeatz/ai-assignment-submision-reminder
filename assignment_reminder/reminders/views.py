import os
import pickle
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from submissions.models import Assignment, StudentSubmission
from django.shortcuts import render, get_object_or_404
from students.models import Course, Enrollment, Unit
from django.http import JsonResponse

now = timezone.now()
    
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
    
    # Get all courses the student is enrolled in
    enrollments = Enrollment.objects.filter(student=student)
    courses = [enrollment.course for enrollment in enrollments]  # List of courses
    units = Unit.objects.filter(course__in=courses)  # Get all units in the courses
    
    print(courses)

    assignments = Assignment.objects.all()
    submissions = StudentSubmission.objects.filter(student=student)

    completed_assignments = sum(1 for sub in submissions if sub.is_submitted)
    unsubmitted_assignments = [assignment for assignment in assignments if not any(sub.assignment.id == assignment.id for sub in submissions)]

    now = timezone.now()
    assignments_deadline = Assignment.objects.filter(
        deadline__gte=now,
        deadline__lte=now + timezone.timedelta(days=7)
    ).exclude(id__in=[sub.assignment.id for sub in submissions if sub.is_submitted])

    return render(request, "assignment_list.html", {
        "assignments": assignments,
        "submissions": submissions,
        "completed_assignments": completed_assignments,
        "unsubmitted_assignments": unsubmitted_assignments,
        "assignments_deadline": assignments_deadline,
        "courses": courses,
        "units": units,  # Pass all units in those courses
    })


@login_required
def enroll(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student_profile = request.user.student_profile
    current_year_category = student_profile.year_category  

    # Get available units for the student's year
    available_units = course.units.filter(available_for_years=current_year_category)

    if request.method == "POST":
        selected_unit_ids = request.POST.getlist("units")  # Get selected units from the form

        if not selected_unit_ids:
            messages.error(request, "You must select at least one unit to enroll.")
            return redirect('enroll', course_id=course.id)

        # Try to find an existing enrollment for this student in this course
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()

        if not enrollment:
            # If no enrollment exists, create a new one
            enrollment = Enrollment.objects.create(student=request.user, course=course)

        # Add selected units to the enrollment (make sure Enrollment has a ManyToManyField to Unit)
        enrollment.units.add(*Unit.objects.filter(id__in=selected_unit_ids))

        messages.success(request, f"You have successfully enrolled in {course.name} and selected {len(selected_unit_ids)} units.")

        return redirect('assignment_list')

    return render(request, 'enroll.html', {
        'course': course,
        'available_units': available_units,
    })

@login_required
def  enroll_course(request):
    courses = Course.objects.all()
    return render(request, 'enroll_course.html', {'courses': courses})

def get_course_for_unit(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return JsonResponse({'course_id': unit.course.id})  # Return the associated course ID
