from django.urls import path
from . import send_reminders

urlpatterns = [
    path('predict/', send_reminders.predict_submission, name='predict_submission'),
]
