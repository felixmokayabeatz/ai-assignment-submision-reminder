from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"