from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import google.generativeai as genai


GEMINI_API_KEY = settings.GEMINI_API_KEY
genai.configure(api_key=GEMINI_API_KEY)

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    course = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if self.deadline and self.deadline.tzinfo is None:
            self.deadline = timezone.make_aware(self.deadline, timezone.get_current_timezone())
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class StudentSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    
    class SubmissionStatus(models.TextChoices):
        NOT_STARTED = 'NS', 'Not Started'
        IN_PROGRESS = 'IP', 'In Progress'
        SUBMITTED_EARLY = 'SE', 'Submitted Early'
        SUBMITTED_ON_TIME = 'ST', 'Submitted On Time'
        LATE_SUBMISSION = 'LS', 'Late Submission'
    
    status = models.CharField(
        max_length=2, 
        choices=SubmissionStatus.choices, 
        default=SubmissionStatus.NOT_STARTED
    )

    ai_feedback = models.TextField(blank=True, null=True)

    def update_status(self):
        now = timezone.now()
        if self.submitted_at:
            if self.submitted_at < self.assignment.deadline:
                self.status = self.SubmissionStatus.SUBMITTED_EARLY if self.submitted_at < self.assignment.deadline - timezone.timedelta(days=2) else self.SubmissionStatus.SUBMITTED_ON_TIME
            else:
                self.status = self.SubmissionStatus.LATE_SUBMISSION
        elif now > self.assignment.deadline:
            self.status = self.SubmissionStatus.LATE_SUBMISSION
        
        self.save()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.submitted_at:
            student_profile = self.student.student_profile
            days_before_deadline = (self.assignment.deadline - self.submitted_at).total_seconds() / 86400
            
            if not hasattr(student_profile.submission_history, 'append'):
                student_profile.submission_history = []
            
            if not self.ai_feedback:
                self.ai_feedback = self.generate_ai_feedback()
                self.save()

    def generate_ai_feedback(self):
        """
        Generate unique AI feedback based on procrastination score and submission history.Make it short as possible
        """
        from google.generativeai import GenerativeModel
        import json

        student_profile = self.student.student_profile
        prompt = f"""
        This student has a procrastination score of {student_profile.procrastination_score} 
        and the following past submission history: {json.dumps(student_profile.submission_history, indent=2)}.
        For the current assignment titled "{self.assignment.title}", their status is "{self.get_status_display()}".

        Generate a unique feedback message to encourage or guide them based on their trends.
        
        Make it short as possible as you can.
        """

        model = GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        try:
            return response.candidates[0].content.parts[0].text.strip()
        except Exception as e:
            print(f"AI feedback generation error: {e}")
            return "Keep improving your submission habits!"  # Fallback message
