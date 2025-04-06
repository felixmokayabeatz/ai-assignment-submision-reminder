from django.shortcuts import render, get_object_or_404, redirect
from .models import Assignment, StudentSubmission
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required  # Only staff/admins can access for now
def student_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = StudentSubmission.objects.filter(assignment=assignment)

    if request.method == 'POST':
        submission_id = request.POST.get('submission_id')
        submission = StudentSubmission.objects.get(id=submission_id)
        submission.marked = True
        submission.save()
        return redirect('student_submissions', assignment_id=assignment.id)

    return render(request, 'instructor/student_submissions.html', {
        'assignment': assignment,
        'submissions': submissions
    })
    
    
    
    
from django.shortcuts import render
from .models import Assignment

def list_assignments(request):
    assignments = Assignment.objects.all()
    return render(request, 'instructor/list_assignments.html', {'assignments': assignments})

