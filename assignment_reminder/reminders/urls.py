from django.urls import path, include
# from . import send_reminders
# from .views import submit_assignment
from .views import assignment_list, submit_assignment, submit_assignment, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    # path('predict/', send_reminders.predict_submission, name='predict_submission'),
    # path("", assignment_list, name="assignment_list"),
    path("assignments/", assignment_list, name="assignment_list"),
     
     
    path("submit/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
]
