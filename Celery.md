
# Celery start worker on the database

celery -A assignment_reminder worker --loglevel=info --pool=solo

# Celery start beat on the database

celery -A assignment_reminder beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
