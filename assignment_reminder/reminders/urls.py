from django.urls import path, include
# from . import send_reminders
# from .views import submit_assignment
from .views import assignment_list, submit_assignment, submit_assignment

urlpatterns = [
    # path('', home, name='land_page'),
    # path('predict/', send_reminders.predict_submission, name='predict_submission'),
    # path("", assignment_list, name="assignment_list"),
    path("assignments/", assignment_list, name="assignment_list"),
     
     
    path("submit/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path("accounts/", include("django.contrib.auth.urls")),
]
