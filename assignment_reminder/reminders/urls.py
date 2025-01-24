from django.urls import path
# from . import send_reminders
from .home import home

urlpatterns = [
    path('', home, name='land_page'),
    # path('predict/', send_reminders.predict_submission, name='predict_submission'),
]
