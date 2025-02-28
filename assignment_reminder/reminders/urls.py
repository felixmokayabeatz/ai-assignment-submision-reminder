from django.urls import path, include
from .views import assignment_list, submit_assignment, submit_assignment, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path("assignments/", assignment_list, name="assignment_list"),
     
     
    path("submit/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
]
