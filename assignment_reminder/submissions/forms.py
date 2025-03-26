from django import forms
from .models import StudentSubmission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentSubmission
        fields = ['student_attachment']
