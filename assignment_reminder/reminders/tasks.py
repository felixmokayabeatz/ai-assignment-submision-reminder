from celery import shared_task
from .views import schedule_reminders

@shared_task
def send_periodic_reminders():
    schedule_reminders()
