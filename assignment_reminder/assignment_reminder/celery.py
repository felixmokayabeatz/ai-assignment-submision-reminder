from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment_reminder.settings')

app = Celery('assignment_reminder')

app.conf.update(
    broker='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))




from celery.schedules import crontab

app.conf.beat_schedule = {
    'send_reminders_every_day_at_9am': {
        'task': 'assignment_reminder.tasks.check_and_send_reminders',  # The full path to the task
        'schedule': crontab(minute=33, hour=16),  # Sends reminders every day at 9:00 AM
    },
    # You can add more schedules if needed
}
