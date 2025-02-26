# Celery

celery -A assignment_reminder beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
